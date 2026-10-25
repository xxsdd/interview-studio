"""Build bounded interview context locally, without extra model requests."""
import json
import bank

QUESTION = {'id':'题库编号','zh':'问题','en':'Question'}
ANSWER_SCHEMA = {
    'organized_zh':'忠于原意的中文','organized_en':'Equivalent English','transcription_note':'没有修正则空字符串',
    'feedback':{'verdict':'一句具体判断','strengths':['结合原话的正确点'],'gaps':['缺漏或错误及原因'],
                'correct_answer':'针对本题完整、连贯的正确参考回答，解释必要的原因和例子；与候选人原答分开','expression':'评价原回答的结构或语言'},
    'next_question':QUESTION,
}
SUMMARY_SCHEMA = {'summary':'总体观察','strengths':['有回答证据的优势'],
                  'priorities':['优先补习的知识'],'next_practice':['可执行的下一次练习建议']}


def shortlist(session, limit=6):
    ids = session['candidates']
    current = session['current']['id']
    visited = {turn['question']['id'] for turn in session['turns']}
    unseen = [i for i in ids if i not in visited and i != current]
    remaining = unseen or [i for i in ids if i != current]
    topic = bank.BY_ID[current]['topic']
    same = [i for i in remaining if bank.BY_ID[i]['topic']==topic]
    other = [i for i in remaining if bank.BY_ID[i]['topic']!=topic]
    # Include nearby questions plus alternatives from different topics.
    diverse = []
    topics = set()
    for ident in other:
        t = bank.BY_ID[ident]['topic']
        if t not in topics:
            diverse.append(ident)
            topics.add(t)
    chosen = [current] if session.get('followup_depth',0)<2 or not remaining else []
    for ident in same[:2]+diverse+remaining:
        if ident not in chosen:
            chosen.append(ident)
        if len(chosen)>=limit:
            break
    return chosen


def excerpt(text, limit):
    if len(text)<=limit:
        return text
    # Preserve both ends and explicitly label omissions; no invented summary.
    return text[:limit*2//3]+'\n[中间内容省略；仅为历史节选]\n'+text[-limit//3:]


def compact_turn(turn, language, summary=False):
    feedback = (turn.get('result') or {}).get('feedback',{})
    item = dict(question_id=turn['question']['id'],question=turn['question'][language],
                raw_answer=excerpt(turn['answer'],1200))
    if len(turn['answer'])>1200:
        item['answer_is_excerpt']=True
    if feedback:
        item['previous_gaps']=[excerpt(v,240) for v in feedback.get('gaps',[])[:3]]
        if summary:
            item['previous_strengths']=[excerpt(v,240) for v in feedback.get('strengths',[])[:3]]
            item['previous_verdict']=excerpt(feedback.get('verdict',''),300)
    return item


def build(session, action):
    language = session['language']
    context = dict(feedback_language=session['feedback_language'],question_language=language)
    refs = []
    if action=='start':
        first=bank.BY_ID[session['candidates'][0]]
        allowed=[first['id']]
        context.update(instruction='开始面试，只问给定首题，可改为真实工作场景。给中英文问题，不透露答案。',
                       first_question=dict(id=first['id'],title=first['title']),schema={'question':QUESTION})
    elif action=='answer':
        turn=session['turns'][-1]
        allowed=shortlist(session)
        refs=bank.references(turn['question']['id'],turn['question'][language]+' '+turn['answer'])
        context.update(instruction='评价当前原始回答，整理并翻译，然后立即给一道追问。next_question.id只能选catalog；depth>=2时换一道主问题。历史节选不代表完整回答，不能把省略当作遗漏。',
                       catalog=[dict(id=i,title=bank.BY_ID[i]['title']) for i in allowed],
                       followup_depth=session.get('followup_depth',0),
                       current_question=turn['question'],raw_answer=turn['answer'],
                       recent_history=[compact_turn(t,language) for t in session['turns'][-3:-1]],
                       source_material=[dict(source=r['source'],text=r['text'],**({'section':r['section']} if r.get('section') else {})) for r in refs],
                       schema=ANSWER_SCHEMA)
    elif action=='summary':
        allowed=[]
        completed=[t for t in session['turns'] if t.get('result')]
        context.update(instruction='依据原始回答和已记录反馈总结实际表现，用反馈语言输出。历史节选不代表完整回答，不把省略当遗漏，不推断录用概率。',
                       recent_history=[compact_turn(t,language,summary=True) for t in completed[-20:]],
                       schema=SUMMARY_SCHEMA)
        if len(completed)>20:
            context['instruction']+=' 仅总结最近20轮，必须在summary说明此范围。'
    else:
        raise ValueError('未知的面试任务。')
    return context,refs,allowed


def serialize(context):
    return json.dumps(context,ensure_ascii=False,separators=(',',':'))
