"""Progress is completed processing steps, not elapsed-time estimation."""
import ai

STEPS = {
    'clarify':[('prepare','读取本题与讨论'),('explanation','解释你的疑问'),('validate','检查解释'),('save','保存讨论')],
    'start':[('prepare','准备题库'),('question','面试官出题'),('validate','检查问题'),('save','保存完成')],
    'answer':[('prepare','准备参考资料'),('organize','整理双语回答'),('feedback','整理面试反馈'),('next_question','准备下一道问题'),('validate','检查内容'),('save','保存完成')],
    'summary':[('prepare','整理本场记录'),('summary','生成面试复盘'),('validate','检查复盘'),('save','保存完成')],
}

def progress(action, stage='prepare', completed=None, detail='', content=''):
    steps = STEPS[action]
    completed = list(dict.fromkeys(completed or []))
    return dict(stage=stage, steps=[dict(id=i,label=label,done=i in completed) for i,label in steps],
                completed=len([i for i,_ in steps if i in completed]), total=len(steps),
                detail=detail, received_chars=len(content))

def streamed_progress(action, content, thinking=False):
    fields, current = ai.complete_fields(content)
    done = ['prepare']
    if action == 'answer':
        if all(k in fields for k in ('organized_zh','organized_en')):
            done.append('organize')
        if 'feedback' in fields:
            done.append('feedback')
        if 'next_question' in fields:
            done.append('next_question')
        if current in ('feedback','next_question'):
            stage = current
        else:
            stage = 'organize'
    else:
        stage = 'explanation' if action=='clarify' else 'question' if action=='start' else 'summary'
        if (action=='start' and 'question' in fields) or (action=='summary' and 'next_practice' in fields):
            done.append(stage)
    detail = '模型正在思考，等待正文' if thinking and not content else '正在接收模型输出'
    return progress(action,stage,done,detail,content)

def normalized_usage(usage):
    usage = usage if isinstance(usage,dict) else {}
    def number(*keys):
        for key in keys:
            value=usage.get(key)
            if isinstance(value,int) and not isinstance(value,bool) and value>=0:
                return value
        return None
    prompt=number('prompt_tokens','input_tokens')
    completion=number('completion_tokens','output_tokens')
    total=number('total_tokens')
    if total is None and prompt is not None and completion is not None:
        total=prompt+completion
    details=usage.get('completion_tokens_details') or usage.get('output_tokens_details') or {}
    reasoning=details.get('reasoning_tokens') if isinstance(details,dict) else None
    return dict(input=prompt,output=completion,total=total,
                reasoning=reasoning if isinstance(reasoning,int) and not isinstance(reasoning,bool) and reasoning>=0 else None)

def aggregate(tasks):
    tasks=[t for t in tasks if t.get('action') in STEPS]
    sums={k:0 for k in ('input','output','total')}
    known={k:0 for k in sums}
    missing={k:0 for k in sums}
    pending=0
    for t in tasks:
        usage=normalized_usage(t.get('usage'))
        is_pending=t['status'] in ('pending','running')
        pending+=int(is_pending)
        for key in sums:
            if usage[key] is not None:
                sums[key]+=usage[key]
                known[key]+=1
            elif not is_pending:
                missing[key]+=1
    return dict(totals={k:sums[k] if known[k] or not tasks else None for k in sums},
                missing=missing,pending=pending,requests=len(tasks),
                note='包括首题、回答、提问讨论、复盘及重试；未返回的用量不按零计算。')
