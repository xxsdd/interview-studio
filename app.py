import json
import secrets
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.background import BackgroundTask
import ai
import bank
import speech
import storage
import telemetry
import prompting
import azure_speech
import library
import study
import answer_contract
import clarification

ROOT = Path(__file__).resolve().parent
APP_TOKEN = secrets.token_urlsafe(32)
POOL = ThreadPoolExecutor(max_workers=3)
ASR_POOL = ThreadPoolExecutor(max_workers=1)
LOCK = threading.RLock()
CONTROLS = {}
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
azure_speech.recover()

for task in storage.all_records('tasks'):
    if task.get('status') in ('pending','running'):
        task.update(status='error', finished=time.time(), error='本地服务重新启动，上一请求未完成。回答已保存；没有自动重新调用 AI。')
        storage.put('tasks', task['id'], task)
        session = storage.get('sessions', task.get('session_id'))
        if session:
            session['busy'] = None
            session['last_task'] = task['id']
            storage.put('sessions', session['id'], session)

@app.middleware('http')
async def local_only(request, call_next):
    host = request.headers.get('host','').split(':')[0]
    if host not in ('127.0.0.1','localhost','testserver'):
        return JSONResponse({'detail':'仅允许本机访问。'}, status_code=403)
    origin = request.headers.get('origin')
    if origin and origin != 'http://' + request.headers.get('host',''):
        return JSONResponse({'detail':'不允许跨站请求。'}, status_code=403)
    if request.method != 'GET' and request.headers.get('x-interview-token') != APP_TOKEN:
        return JSONResponse({'detail':'页面已过期，请刷新后再试。'}, status_code=403)
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; media-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'"
    return response

@app.exception_handler(ValueError)
async def invalid(request, exc):
    return JSONResponse({'detail':str(exc)}, status_code=400)

def session_get(sid, include_deleted=False):
    session = storage.get('sessions', sid)
    if not session or (session.get('deleted_at') and not include_deleted):
        raise HTTPException(404, '找不到这场练习。')
    return session

def task_public(task):
    control=CONTROLS.get(task['id'])
    return {**{k:v for k,v in task.items() if k not in ('raw','provider','context')},
            'cancel_requested':bool(control and control.stopped.is_set()),
            'has_saved_response':bool(task.get('raw','').strip()),
            'tokens':telemetry.normalized_usage(task.get('usage'))}

@app.get('/api/health')
def health():
    return {'app':'interview-studio','questions':len(bank.QUESTIONS)}

@app.post('/api/speak')
def speak(body:dict):
    raise HTTPException(410,'朗读入口已更新，请刷新页面后点击问题下方的朗读按钮。')

@app.get('/api/speech/settings')
def speech_settings():
    return dict(settings=azure_speech.public_settings(),usage=azure_speech.usage())

@app.post('/api/speech/settings')
def save_speech_settings(body:dict):
    return dict(settings=azure_speech.save_settings(body),usage=azure_speech.usage())

@app.post('/api/speech/voices')
def speech_voices(body:dict):
    return dict(voices=azure_speech.voices(bool(body.get('refresh'))))

@app.post('/api/speech/jobs')
def speech_job_create(body:dict):
    language=body.get('language')
    if language not in ('zh','en'):
        raise ValueError('请选择中文或英文。')
    sid=body.get('session_id')
    if body.get('preview') is True:
        text=azure_speech.PREVIEWS[language]
        sid=None
    else:
        s=session_get(sid)
        text=str(body.get('text','')).strip()
        questions=[t['question'] for t in s['turns']]+([s['current']] if s.get('current') else [])
        if not text or len(text)>6000 or text not in {q[language].strip() for q in questions}:
            raise ValueError('只能朗读本场已有的面试官问题。')
    return azure_speech.submit(text,language,sid,body.get('voice'))

@app.get('/api/speech/jobs/{ident}')
def speech_job(ident:str):
    job=storage.get('speech_jobs',ident)
    if not job:
        raise HTTPException(404,'语音请求不存在。')
    return azure_speech.job_public(job)

@app.get('/api/speech/audio/{ident}')
def speech_audio(ident:str):
    return FileResponse(azure_speech.audio_path(ident),media_type='audio/mpeg')

@app.get('/api/bootstrap')
def bootstrap():
    return dict(token=APP_TOKEN, settings=storage.public_settings(), catalog=bank.catalog(), speech=speech.available())

@app.get('/api/settings')
def settings():
    return storage.public_settings()

@app.get('/api/subscription/status')
def subscription_status():
    import subscription
    return subscription.status()

@app.post('/api/settings')
def settings_save(body:dict):
    return storage.save_settings(body)

@app.post('/api/models/discover')
def models_discover(body:dict):
    return ai.discover_models(body)

@app.get('/api/source/{source_id}')
def source(source_id:str):
    if source_id in library.DOCUMENTS:
        return library.DOCUMENTS[source_id]
    for d in bank.DOCUMENTS:
        if d['id'] == source_id:
            return d
    raise HTTPException(404, '资料不存在。')

@app.get('/api/library')
def library_catalog():
    return library.catalog()

@app.get('/api/library/{ident}')
def library_detail(ident:str):
    return library.detail(ident)

@app.post('/api/library/{ident}/learned')
def library_learned(ident:str,body:dict):
    with LOCK:
        u=library.unit(ident)
        p=library.progress(u)
        p['learned']=body.get('learned') is True
        storage.put('study_progress',library.key(u),p)
        for s in storage.all_records('sessions'):
            if s.get('mode')=='study' and library.key(s['study_unit'])==library.key(u):
                s['study_progress']['learned']=p['learned']
                storage.put('sessions',s['id'],s)
        return library.detail(ident)

@app.get('/api/question/{qid}')
def question(qid:str):
    if qid not in bank.BY_ID:
        raise HTTPException(404, '题目不存在。')
    return bank.BY_ID[qid]

@app.get('/api/sessions')
def sessions():
    return sorted([dict(id=s['id'], title=s['title'], created=s['created'], status=s['status'], turns=len(s['turns']), busy=s.get('busy'))
                   for s in storage.all_records('sessions') if not s.get('deleted_at')], key=lambda s:s['created'], reverse=True)

@app.get('/api/trash')
def trash_list():
    return sorted([dict(id=s['id'],title=s['title'],created=s['created'],deleted_at=s['deleted_at'],turns=len(s['turns']))
                   for s in storage.all_records('sessions') if s.get('deleted_at')],key=lambda s:s['deleted_at'],reverse=True)

@app.post('/api/sessions/{sid}/trash')
def trash_session(sid:str):
    with LOCK:
        s=session_get(sid,include_deleted=True)
        if s.get('busy'):
            raise ValueError('本场正在处理中，完成后可以删除。')
        s['deleted_at']=s.get('deleted_at') or time.time()
        storage.put('sessions',sid,s)
    return {'ok':True}

@app.post('/api/sessions/{sid}/restore')
def restore_session(sid:str):
    with LOCK:
        s=session_get(sid,include_deleted=True)
        s.pop('deleted_at',None)
        storage.put('sessions',sid,s)
    return {'ok':True}

@app.get('/api/sessions/{sid}')
def session(sid:str):
    s=session_get(sid)
    s['usage_summary']=telemetry.aggregate([t for t in storage.all_records('tasks') if t.get('session_id')==sid])
    if s.get('mode')=='study':
        s['study_usage']=library.usage(s['study_unit'])
    return s

@app.get('/api/tasks/{tid}')
def task(tid:str):
    t = storage.get('tasks',tid)
    if not t:
        raise HTTPException(404,'请求不存在。')
    return task_public(t)

def enqueue(session, action, provider, extra=None):
    tid = uuid.uuid4().hex
    task = dict(id=tid, session_id=session['id'], action=action, status='pending', created=time.time(), output_limit=ai.OUTPUT_TOKEN_LIMIT, **(extra or {}))
    task['progress']=telemetry.progress(action,detail='请求已排队')
    session['busy'] = tid
    storage.put('sessions',session['id'],session)
    storage.put('tasks',tid,task)
    CONTROLS[tid]=ai.GenerationControl()
    POOL.submit(run_task,tid,provider)
    return dict(task_id=tid, session_id=session['id'])

@app.post('/api/tasks/{tid}/cancel')
def cancel_task(tid:str):
    with LOCK:
        t=storage.get('tasks',tid)
        if not t:raise HTTPException(404,'请求不存在。')
        session_get(t['session_id'])
        if t['status'] not in ('pending','running'):return {'stopping':False,'status':t['status']}
        control=CONTROLS.get(tid)
        if not control:raise ValueError('此请求无法停止，请刷新页面检查状态。')
        control.stop()
        return {'stopping':True}

@app.post('/api/sessions')
def start(body:dict):
    with LOCK:
        request_id = str(body.get('request_id',''))
        if not request_id or len(request_id)>80:
            raise ValueError('请求编号缺失。')
        previous = storage.get('requests',request_id)
        if previous:
            return previous
        p = ai.provider_snapshot()
        topic = body.get('topic','all')
        if topic != 'all' and topic not in bank.TOPICS:
            raise ValueError('请选择有效主题。')
        language = 'en' if body.get('language') == 'en' else 'zh'
        feedback_language = 'en' if body.get('feedback_language') == 'en' else 'zh'
        candidates = [q for q in bank.QUESTIONS if topic == 'all' or q['topic'] == topic]
        session = dict(id=uuid.uuid4().hex, title='综合摸底' if topic=='all' else topic,
                       topic=topic, language=language, feedback_language=feedback_language,
                       created=time.time(), status='active', current=None, turns=[], summary=None,
                       candidates=[q['id'] for q in candidates], followup_depth=0)
        if body.get('mode')=='study':
            u=library.unit(body.get('unit_id'))
            existing=next((s for s in storage.all_records('sessions') if s.get('mode')=='study' and not s.get('deleted_at') and s['status']=='active' and library.key(s['study_unit'])==library.key(u)),None)
            if existing:
                result=dict(session_id=existing['id'],task_id=existing.get('busy'),resumed=True)
                storage.put('requests',request_id,result)
                return result
            study.initialize(session,u['id'])
        result = enqueue(session,'start',p)
        storage.put('requests',request_id,result)
        return result

@app.post('/api/sessions/{sid}/answer')
def answer(sid:str, body:dict):
    with LOCK:
        s = session_get(sid)
        request_id = str(body.get('request_id',''))
        if not request_id or len(request_id)>80:
            raise ValueError('请求编号缺失。')
        previous = storage.get('requests',request_id)
        if previous:
            return previous
        if s.get('busy') or not s.get('current') or s.get('awaiting_continue') or s['status'] != 'active':
            raise ValueError('请等当前处理结束后再提交。')
        if s['turns'] and not s['turns'][-1].get('result'):
            raise ValueError('上一回答尚未完成，请使用重试按钮。')
        text = str(body.get('text','')).strip()
        if not text or len(text)>12000:
            raise ValueError('请输入 1 至 12000 字的回答。')
        p = ai.provider_snapshot()
        s['language'] = 'en' if body.get('language') == 'en' else 'zh'
        s['feedback_language'] = 'en' if body.get('feedback_language') == 'en' else 'zh'
        turn = dict(id=uuid.uuid4().hex, question=s['current'], answer=text,
                    created=time.time(), result=None, refs=[], input_language=body.get('input_language','auto'))
        s['turns'].append(turn)
        result = enqueue(s,'answer',p,dict(turn_id=turn['id']))
        storage.put('requests',request_id,result)
        return result

@app.post('/api/sessions/{sid}/continue')
def continue_study(sid:str):
    with LOCK:
        s=session_get(sid)
        if s.get('mode')!='study' or s['status']!='active' or s.get('busy') or not s.get('awaiting_continue') or not s.get('current'):
            raise ValueError('当前没有待继续的问题。')
        s['awaiting_continue']=False
        storage.put('sessions',sid,s)
        return {'session_id':sid}

@app.post('/api/sessions/{sid}/clarify')
def ask_clarification(sid:str, body:dict):
    with LOCK:
        s=session_get(sid)
        request_id=str(body.get('request_id',''))
        if not request_id or len(request_id)>80:
            raise ValueError('请求编号缺失。')
        previous=storage.get('requests',request_id)
        if previous:
            return previous
        if s.get('busy'):
            raise ValueError('请等当前处理完成后再提问。')
        turn=next((t for t in s['turns'] if t['id']==body.get('turn_id')),None)
        if not turn or not turn.get('result'):
            raise ValueError('请先选择一条已完成的反馈。')
        text=str(body.get('text','')).strip()
        if not text or len(text)>12000:
            raise ValueError('请输入 1 至 12000 字的问题。')
        provider=ai.provider_snapshot()
        item=dict(id=uuid.uuid4().hex,question=text,created=time.time(),answer=None)
        turn.setdefault('clarifications',[]).append(item)
        result=enqueue(s,'clarify',provider,dict(turn_id=turn['id'],clarification_id=item['id']))
        storage.put('requests',request_id,result)
        return result

@app.post('/api/sessions/{sid}/summary')
def summarize(sid:str):
    with LOCK:
        s = session_get(sid)
        if s.get('busy') or not s['turns'] or not s['turns'][-1].get('result'):
            raise ValueError('完成至少一道题并收到反馈后，才能结束并复盘。')
        if s['status'] == 'completed':
            raise ValueError('本场已经结束。')
        return enqueue(s,'summary',ai.provider_snapshot())

@app.post('/api/tasks/{tid}/retry')
def retry(tid:str):
    with LOCK:
        previous = storage.get('tasks',tid)
        if not previous or previous['status'] != 'error' or previous['action'] == 'asr':
            raise ValueError('当前请求不能重试。')
        s = session_get(previous['session_id'])
        if s.get('busy'):
            raise ValueError('正在处理中。')
        if s.get('last_task') != tid:
            raise ValueError('此请求已有后续重试，请刷新页面。')
        if previous.get('raw'):
            try:
                restored=recover_saved(tid)
                return dict(task_id=tid,session_id=restored['session_id'],recovered=True)
            except ValueError:
                pass
        result = enqueue(s,previous['action'],ai.provider_snapshot(),dict(turn_id=previous.get('turn_id'),clarification_id=previous.get('clarification_id')))
        previous['retry_task'] = result['task_id']
        storage.put('tasks',tid,previous)
        return result

@app.get('/api/tasks/{tid}/saved')
def saved_response(tid:str):
    t=storage.get('tasks',tid)
    if not t or not t.get('raw'): raise HTTPException(404,'没有已保存的模型返回。')
    session_get(t['session_id'])
    return {'text':t['raw']}

def commit_result(t,result,refs):
    with LOCK:
        s=session_get(t['session_id']); is_study=s.get('mode')=='study'
        if t['action']=='clarify':
            _,item=clarification.locate(s,t)
            if item.get('answer'):
                raise ValueError('此提问已完成，不能覆盖已有解释。')
            item.update(answer=result['explanation'],usage=t.get('usage'),model=t.get('model'),finished=time.time())
        elif t['action']=='start': s['current']=result['question']
        elif t['action']=='answer':
            turn=s['turns'][-1]
            turn.update(result=result,refs=[{k:v for k,v in r.items() if k!='text'} for r in refs],usage=t.get('usage'),model=t.get('model'))
            if not is_study:
                same=result['next_question']['id']==s['current']['id']
                s['followup_depth']=s['followup_depth']+1 if same else 0
                s['current']=result['next_question']
        else: s.update(summary=result,status='completed')
        s.update(busy=None,last_task=t['id'])
        if is_study and t['action']!='clarify':
            study.apply(s,result,t['action']);study.persist(s)
        else: storage.put('sessions',s['id'],s)

@app.post('/api/tasks/{tid}/recover')
def recover_saved(tid:str):
    with LOCK:
        t=storage.get('tasks',tid)
        if not t or not t.get('raw') or t.get('action') not in ('start','answer','summary','clarify'):
            raise ValueError('没有可恢复的已保存返回。')
        s=session_get(t['session_id'])
        if s.get('busy') or s.get('last_task')!=tid:
            raise ValueError('练习已有后续处理，不能覆盖当前进度。')
        if t['status']=='done' and t.get('recovered_at'):
            return dict(session_id=s['id'],recovered=True)
        if t['status']!='error':raise ValueError('此结果无需恢复。')
        if t['action']=='start' and (s.get('current') or s['turns']):raise ValueError('首题已有后续进度。')
        if t['action']=='answer' and (not s['turns'] or s['turns'][-1]['id']!=t.get('turn_id') or s['turns'][-1].get('result')):
            raise ValueError('该回答已有后续进度。')
        if t['action']=='summary' and s.get('summary'):raise ValueError('已有复盘。')
        is_study=s.get('mode')=='study'
        _,refs,ids=clarification.build(s,t) if t['action']=='clarify' else (study.build if is_study else prompting.build)(s,t['action'])
        parsed=ai.parse(t['raw'])
        result=clarification.validate(parsed) if t['action']=='clarify' else study.validate(parsed,s,t['action'],ids) if is_study else ai.validate(parsed,t['action'],ids)
        commit_result(t,result,refs)
        t['recovered_error']=t.pop('error','')
        t.update(status='done',recovered_at=time.time(),progress=telemetry.progress(t['action'],'save',[k for k,_ in telemetry.STEPS[t['action']]],'已从本机保存的返回恢复，未重新调用 AI',t['raw']))
        storage.put('tasks',tid,t)
        return dict(session_id=s['id'],recovered=True)

def run_task(tid, provider):
    t = storage.get('tasks',tid)
    control=CONTROLS.setdefault(tid,ai.GenerationControl())
    try:
        control.check()
        t['status'] = 'running'
        storage.put('tasks',tid,t)
        s = session_get(t['session_id'])
        is_study=s.get('mode')=='study'
        context, refs, ids = clarification.build(s,t) if t['action']=='clarify' else (study.build if is_study else prompting.build)(s,t['action'])
        rules=clarification.RULES if t['action']=='clarify' else study.RULES if is_study else ai.RULES
        if t['action']!='clarify':
            rules+='\n'+answer_contract.OUTPUT_RULES
        context_text = prompting.serialize(context)
        stage='explanation' if t['action']=='clarify' else 'organize' if t['action']=='answer' else 'question' if t['action']=='start' else 'summary'
        t.update(progress=telemetry.progress(t['action'],stage,['prepare'],'等待模型响应'),
                 model=provider['model'],provider_name=provider['name'],reasoning_effort=provider.get('reasoning_effort'),
                 prompt_info=dict(version='study-v1' if is_study else 'compact-v1',characters=len(rules)+len(context_text),
                                  candidate_questions=len(ids),reference_characters=sum(len(b['text']) for b in context.get('source_blocks',[])) if is_study else sum(len(r['text']) for r in refs)))
        storage.put('tasks',tid,t)
        last_write=0
        def update_stream(content,usage,thinking):
            nonlocal last_write
            old_stage=t['progress']['stage']
            t.update(raw=content,usage=usage,progress=telemetry.streamed_progress(t['action'],content,thinking))
            now=time.monotonic()
            if now-last_write>=.4 or old_stage!=t['progress']['stage'] or usage:
                storage.put('tasks',tid,t)
                last_write=now
            control.check()
        update_stream.control=control
        content, usage = ai.call([{'role':'system','content':rules},
                                  {'role':'user','content':context_text}],provider,on_progress=update_stream)
        t.update(raw=content, usage=usage, model=provider['model'], provider_name=provider['name'])
        completed=[key for key,_ in telemetry.STEPS[t['action']] if key not in ('validate','save')]
        t['progress']=telemetry.progress(t['action'],'validate',completed,'模型已返回，正在检查内容',content)
        storage.put('tasks',tid,t)
        parsed=ai.parse(content)
        result = clarification.validate(parsed) if t['action']=='clarify' else study.validate(parsed,s,t['action'],ids) if is_study else ai.validate(parsed,t['action'],ids)
        t['progress']=telemetry.progress(t['action'],'save',completed+['validate'],'正在保存',content)
        storage.put('tasks',tid,t)
        with LOCK:
            control.check()
            commit_result(t,result,refs)
            t.update(status='done',finished=time.time(),progress=telemetry.progress(t['action'],'save',completed+['validate','save'],'已完成',content))
            storage.put('tasks',tid,t)
    except Exception as exc:
        message = str(exc) if isinstance(exc, ValueError) else '处理未完成。回答已保存，请检查设置后重试。'
        if control.stopped.is_set():message='已停止生成，接收内容已保存在本机；已产生的用量可能仍会计费，未自动重试。'
        t.update(status='error',error=message,finished=time.time())
        with LOCK:
            s = session_get(t['session_id'])
            s.update(busy=None,last_task=tid)
            storage.put('sessions',s['id'],s)
    storage.put('tasks',tid,t)
    with LOCK:CONTROLS.pop(tid,None)

@app.post('/api/transcribe')
async def transcribe(request:Request):
    length = int(request.headers.get('content-length','0'))
    if length>25_000_000:
        raise ValueError('录音过大，请将一次回答控制在 5 分钟以内。')
    chunks = bytearray()
    async for chunk in request.stream():
        chunks.extend(chunk)
        if len(chunks)>25_000_000:
            raise ValueError('录音过大。')
    if not chunks:
        raise ValueError('没有收到录音。')
    language = request.query_params.get('language','auto')
    if language not in ('zh','en','auto'):
        raise ValueError('无效的录音语言。')
    with LOCK:
        if any(t['action']=='asr' and t['status'] in ('pending','running') for t in storage.all_records('tasks')):
            raise ValueError('已有录音正在识别，请稍后再试。')
        tid = uuid.uuid4().hex
        path = storage.DATA / (tid+'.audio')
        path.write_bytes(chunks)
        storage.put('tasks',tid,dict(id=tid,action='asr',status='pending',created=time.time()))
        ASR_POOL.submit(run_asr,tid,path,language,storage.settings()['device'])
    return dict(task_id=tid)

def run_asr(tid,path,language,device):
    t = storage.get('tasks',tid)
    try:
        t['status']='running'
        storage.put('tasks',tid,t)
        result = speech.transcribe(path,language,device)
        t.update(status='done',result=result)
    except Exception as exc:
        t.update(status='error',error=str(exc) if isinstance(exc,ValueError) else '本地语音识别失败。可在 AI 设置里改为 CPU 后重试，或直接输入文字。')
    finally:
        path.unlink(missing_ok=True)
    storage.put('tasks',tid,t)

@app.get('/')
def index():
    return FileResponse(ROOT/'static'/'index.html')

app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')
