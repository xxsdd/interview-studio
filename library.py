"""Local textbook snapshots, source-bounded lessons and revision-specific progress."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote
import storage

ROOT = Path(__file__).resolve().parent / 'library'
BOOKS = {'01':'入门与知识库','02':'RAG 专项教程','03':'Agent 专项教程','04':'大模型综合参考','05':'面试练习'}
UNITS = {}
DOCUMENTS = {}
WEEKS = []

def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()[:20]

def sections(text, title):
    """Split at real H2s (never code headings), retaining every body paragraph."""
    heading, lines, fenced = '导读', [], False
    for line in text.splitlines():
        if line.strip().startswith(('```','~~~')):
            fenced = not fenced
        if not fenced and line.startswith('## '):
            if heading=='导读':
                # Keep introductory context with the first real section, not as a fake lesson.
                heading=line[3:].strip()
                continue
            if '\n'.join(lines).strip():
                yield heading, '\n'.join(lines).strip()
            heading, lines = line[3:].strip(), []
        else:
            if not fenced and (line.startswith('[书架]') or line.startswith('[返回') or line.strip()=='---'):
                continue
            lines.append(line)
    if '\n'.join(lines).strip():
        yield heading if heading!='导读' else title, '\n'.join(lines).strip()

def blocks(text, limit=1100):
    # Keep all source content; very long paragraphs/code are explicitly split.
    chunks, current = [], ''
    for para in re.split(r'\n\s*\n',text):
        for start in range(0,len(para),limit):
            piece=para[start:start+limit]
            if current and len(current)+len(piece)+2>limit:
                chunks.append(current); current=''
            current += ('\n\n' if current else '')+piece
    if current: chunks.append(current)
    return chunks

def load():
    manifest=ROOT/'manifest.json'
    if not manifest.exists(): return
    for doc in json.loads(manifest.read_text(encoding='utf-8')):
        text=(ROOT/doc['file']).read_text(encoding='utf-8-sig')
        source='textbook-'+digest(doc['file'])
        DOCUMENTS[source]=dict(id=source,title=doc['title'],text=text)
        seen={}
        for title, body in sections(text,doc['title']):
            if len(re.sub(r'[#\s*\-_]','',body))<35: continue
            count=seen.get(title,0); seen[title]=count+1
            parts=blocks(body)
            for offset in range(0,len(parts),5):
                batch=parts[offset:offset+5]
                ident='unit-'+digest(doc['file']+'|'+title+'|'+str(count)+'|'+str(offset//5))
                revision=digest('\n'.join(batch))
                UNITS[ident]=dict(id=ident,book=doc['book'],chapter=' / '.join(filter(None,[doc['group'],doc['title']])),
                    title=title+(f'（分段 {offset//5+1}）' if len(parts)>5 else ''),source=source,revision=revision,
                    blocks=[dict(id=f'b{i+1}',text=t) for i,t in enumerate(batch)])
    load_schedule()

def load_schedule():
    """Add a full-article view without changing legacy units or their progress."""
    path=ROOT/'study-schedule.md'
    if not path.exists():return
    docs={d['file']:d for d in json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))}
    plan_text=path.read_text(encoding='utf-8-sig')
    DOCUMENTS['study-schedule']=dict(id='study-schedule',title='三周实战学习计划',text=plan_text)
    week=None
    for line in plan_text.splitlines():
        match=re.match(r'## (第[一二三]周)：(.+)',line)
        if match:
            week=dict(id='week-'+str(len(WEEKS)+1),title=match[1]+'：'+match[2],articles=[],days=[])
            WEEKS.append(week)
        if not week or not re.match(r'^\| 第 \d+ 天',line):continue
        cells=line.split('|')[1:-1]
        day=int(re.search(r'第 (\d+) 天',cells[0])[1])
        week['days'].append(dict(day=day,practice=cells[2].strip(),goal=cells[3].strip()))
        for label,href in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',cells[1]):
            file=unquote(href)
            if file not in docs:raise ValueError('学习计划关联文章缺失：'+label)
            doc=docs[file];ident='article-'+digest(file)
            if ident not in UNITS:
                raw=(ROOT/file).read_text(encoding='utf-8-sig')
                # Navigation only is removed; all prose, headings, tables and code remain.
                body='\n'.join(l for l in raw.splitlines() if not l.startswith(('[书架]','[返回'))).strip()
                pieces=blocks(body,3500)
                UNITS[ident]=dict(id=ident,book='plan',chapter=doc['title'],title=doc['title'],
                    source='textbook-'+digest(file),revision=digest(body),full_article=True,
                    original_book=doc['book'],original_group=doc['group'],week_ids=[],schedule_days=[],
                    blocks=[dict(id=f'b{i+1}',text=t) for i,t in enumerate(pieces)])
            u=UNITS[ident]
            if week['id'] not in u['week_ids']:u['week_ids'].append(week['id'])
            if day not in u['schedule_days']:u['schedule_days'].append(day)
            if ident not in week['articles']:week['articles'].append(ident)

def unit(ident):
    if ident not in UNITS: raise ValueError('请选择有效的教材小节。')
    return UNITS[ident]

def key(u): return u['id']+'-'+u['revision']

def progress(u):
    return storage.get('study_progress',key(u),{'learned':False,'points':{}})

def plan(u): return storage.get('study_plans',key(u))

def stats(u, progress_map=None, plan_map=None):
    p=progress(u) if progress_map is None else progress_map.get(key(u),{'learned':False,'points':{}})
    points=((plan(u) if plan_map is None else plan_map.get(key(u))) or {}).get('points',[])
    states=p.get('points',{})
    covered=sum(states.get(x['id'],{}).get('attempts',0)>0 for x in points)
    passed=sum(states.get(x['id'],{}).get('status')=='passed' for x in points)
    return dict(total=len(points),covered=covered,passed=passed,learned=p['learned'],complete=bool(points) and passed==len(points))

def catalog():
    with storage.db() as db:
        ps={i:json.loads(b) for i,b in db.execute("SELECT id,body FROM records WHERE kind='study_progress'")}
        plans={i:json.loads(b) for i,b in db.execute("SELECT id,body FROM records WHERE kind='study_plans'")}
    return dict(books=([dict(id='plan',title='三周实战学习计划') ] if WEEKS else [])+[dict(id=k,title=v) for k,v in BOOKS.items()],
        documents=len([k for k in DOCUMENTS if k!='study-schedule']),weeks=WEEKS,
        units=[{**{k:v for k,v in u.items() if k not in ('blocks',)},**stats(u,ps,plans)} for u in UNITS.values()])

def detail(ident):
    u=unit(ident); p=progress(u)
    return {**u,'text':'\n\n'.join(b['text'] for b in u['blocks']), 'progress':p,'plan':plan(u),'stats':stats(u),'usage':usage(u)}

def usage(u):
    import telemetry
    sessions={s['id'] for s in storage.all_records('sessions') if s.get('mode')=='study' and key(s['study_unit'])==key(u)}
    return telemetry.aggregate([t for t in storage.all_records('tasks') if t.get('session_id') in sessions])

load()
