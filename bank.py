"""Offline question catalog and bounded reference retrieval. No provider calls."""
import re
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'bank'
QUESTIONS = []
DOCUMENTS = []
CHUNKS = []
TOPICS = {}
for path in sorted(ROOT.rglob('*.md')):
    text = path.read_text(encoding='utf-8-sig')
    doc_id = f'doc-{len(DOCUMENTS) + 1}'
    title_match = re.search(r'^# (.+)', text, re.M)
    title = title_match.group(1) if title_match else path.stem
    DOCUMENTS.append(dict(id=doc_id, title=title, path=str(path.relative_to(ROOT)), text=text))
    if '01 综合题库' in str(path):
        topic = ''
        for piece in re.split(r'(?=^## |^### Q)', text, flags=re.M):
            if piece.startswith('## '):
                topic = piece.splitlines()[0][3:]
                TOPICS[topic] = 0
            match = re.match(r'### (Q\d+-\d+)\. (.+)', piece)
            if match:
                importance = re.search(r'\*\*重要度：\*\*`([^`]+)', piece)
                difficulty = re.search(r'\*\*难度：\*\*`([^`]+)', piece)
                item = dict(id=match[1], title=match[2], topic=topic,
                            importance=importance[1] if importance else '专题',
                            difficulty=difficulty[1] if difficulty else '中等',
                            text=piece, source=doc_id)
                QUESTIONS.append(item)
                TOPICS[topic] += 1
    else:
        for part in re.split(r'(?=^#{1,3} )', text, flags=re.M):
            if len(part.strip()) > 80:
                for start in range(0, len(part), 3500):
                    CHUNKS.append(dict(source=doc_id, title=title, text=part[start:start+3800]))

BY_ID = {q['id']: q for q in QUESTIONS}

def terms(text):
    low = text.lower()
    return set(re.findall(r'[a-z][a-z0-9_-]{1,}', low) +
               [low[i:i+2] for i in range(len(low)-1) if '\u4e00' <= low[i] <= '\u9fff' and '\u4e00' <= low[i+1] <= '\u9fff'])

def reference_text(text):
    """Keep source prose verbatim; omit navigation and URL destinations."""
    lines = []
    for line in text.splitlines():
        if re.match(r'^\s*(\[书架\]|\*\*(对应章节|重要度|难度)：)', line):
            continue
        line = re.sub(r'\[([^\]]+)\]\((?:<[^>]*>|[^)]*)\)', r'\1', line)
        lines.append(line)
    return '\n'.join(lines).strip()


# Paragraphs are extracted once locally, not summarized by another model.
SNIPPETS = []
for document in DOCUMENTS:
    if any(q['source'] == document['id'] for q in QUESTIONS):
        continue
    heading = ''
    for block in re.split(r'\n\s*\n', reference_text(document['text'])):
        if block.startswith('#'):
            heading, _, block = block.partition('\n')
            heading = heading.lstrip('# ').strip()
        block = block.strip()
        if 60 <= len(block) <= 600:
            SNIPPETS.append(dict(source=document['id'],title=document['title'],
                                 text=block,section=heading[:100],keys=terms(block)))

TERM_COUNTS = Counter(key for snippet in SNIPPETS for key in snippet['keys'])
STOP_TERMS = terms('什么 为什么 怎么 如何 核心 区别 能不能 一起 时候 场景 面试 面试官 问题 回答 这里 一个 哪个 哪些 可以 更好 需要 使用 选择 理解 实际 应该 如果 还是 公司')


def relevance(snippet, keys):
    matched=keys & snippet['keys']
    return sum(math.log(1+len(SNIPPETS)/(1+TERM_COUNTS[k])) for k in matched) / max(1,len(snippet['keys']))**.5


def references(question_id, query):
    primary = BY_ID.get(question_id, QUESTIONS[0])
    text = reference_text(primary['text'])
    keys = terms(query + ' ' + primary['title']) - STOP_TERMS
    anchors = terms(primary['title']) - STOP_TERMS
    ranked = sorted(SNIPPETS, key=lambda c: relevance(c,keys), reverse=True)
    results = [dict(id=primary['id'], title=primary['title'], text=text, source=primary['source'])]
    seen_sources = {primary['source']}
    seen_texts = [terms(p) for p in re.split(r'\n\s*\n',text) if len(p)>30]
    for snippet in ranked:
        candidate_keys = snippet['keys']
        if snippet['source'] in seen_sources or len(keys & candidate_keys)<3 or not anchors & candidate_keys:
            continue
        if re.search(r'可以看|相关阅读|参见|延伸阅读',snippet['text']):
            continue
        # Avoid repeating the primary answer or nearly identical excerpts.
        if any(len(candidate_keys & old)/max(1,len(candidate_keys | old))>=.65 for old in seen_texts):
            continue
        results.append(dict(id=snippet['source'],**{k:v for k,v in snippet.items() if k!='keys'}))
        seen_sources.add(snippet['source'])
        seen_texts.append(candidate_keys)
        if len(results)==2:
            break
    return results

def catalog():
    return dict(count=len(QUESTIONS), documents=len(DOCUMENTS), topics=TOPICS,
                questions=[{k:v for k,v in q.items() if k != 'text'} for q in QUESTIONS],
                sources=[{k:v for k,v in d.items() if k != 'text'} for d in DOCUMENTS])
