"""Azure standard neural questions only; persistent local cache and spending guard."""
import base64
import copy
import hashlib
import html
import json
import re
import threading
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import storage

LOCK = threading.RLock()
VOICE_LOCK = threading.Lock()
POOL = ThreadPoolExecutor(max_workers=2)
MAX_MONTHLY = 450_000  # Below the resource's 500,000 F0 allowance.
PREVIEWS = {'zh':'你好，我们开始面试吧。请介绍一下你的思路。',
            'en':"Hello. Let's begin the interview. Please walk me through your approach."}
DEFAULTS = dict(region='westus2',resource='interview-speech-free-20261015',key='',
                voice_zh='zh-CN-XiaoxiaoNeural',voice_en='en-US-JennyNeural',monthly_limit=MAX_MONTHLY)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('微软语音地址发生跳转，已停止请求。')


def config():
    return {**DEFAULTS, **storage.get('speech_settings','main',{})}


def public_settings():
    value=config()
    value['has_key']=bool(value.pop('key'))
    return value


def safe_voice(voice):
    return (isinstance(voice,str) and re.fullmatch(r'(?:zh-(?:CN|TW|HK)|en-(?:US|CA|GB|AU))-[A-Za-z]+Neural',voice)
            and not any(v in voice for v in ('Multilingual','Dragon','HD','Turbo','MAI','Custom')))


def save_settings(body):
    value=config()
    region=str(body.get('region',value['region'])).strip().lower()
    resource=str(body.get('resource',value['resource'])).strip().lower()
    if not re.fullmatch('[a-z][a-z0-9]{1,40}',region) or not re.fullmatch('[a-z0-9][a-z0-9-]{1,62}',resource):
        raise ValueError('请填写有效的 Azure 区域和资源名称。')
    limit=body.get('monthly_limit',value['monthly_limit'])
    if isinstance(limit,bool) or not isinstance(limit,int) or not 1<=limit<=MAX_MONTHLY:
        raise ValueError('本机月保护上限必须为 1 至 450,000 字符单位。')
    for lang in ('zh','en'):
        voice=body.get('voice_'+lang,value['voice_'+lang])
        if not safe_voice(voice) or not voice.startswith(lang+'-'):
            raise ValueError('仅支持中文或英文的普通 Neural 音色。')
        value['voice_'+lang]=voice
    key=str(body.get('api_key','')).strip()
    if value['region']!=region or value['resource']!=resource:
        value['key']=''
    if body.get('clear_key'):
        value['key']=''
    elif key:
        if not re.fullmatch('[A-Za-z0-9_-]{16,256}',key):
            raise ValueError('微软语音密钥格式不正确。')
        value['key']=base64.b64encode(storage.crypt(key.encode())).decode()
    value.update(region=region,resource=resource,monthly_limit=limit)
    with LOCK:
        storage.put('speech_settings','main',value)
    return public_settings()


def endpoint(c):
    return 'https://'+c['region']+'.tts.speech.microsoft.com'


def resource_id(c):
    return c['region']+'/'+c['resource']


def month():
    return datetime.now(timezone.utc).strftime('%Y-%m')


def units(text):
    # Conservative count: XML escapes may overcount, CJK code points count twice.
    escaped=html.escape(text,quote=False)
    return len(escaped)+sum(1 for ch in text if any(a<=ord(ch)<=b for a,b in (
        (0x3400,0x4DBF),(0x4E00,0x9FFF),(0xF900,0xFAFF),(0x20000,0x2FA1F),(0x30000,0x323AF))))


def usage(c=None):
    c=c or config();current=month();rid=resource_id(c)
    events=[e for e in storage.all_records('speech_events') if e.get('resource')==rid and e.get('month')==current]
    used=sum(e['units'] for e in events if e['status']=='success')
    uncertain=sum(e['units'] for e in events if e['status']!='success')
    hits=[j for j in storage.all_records('speech_jobs') if j.get('resource')==rid and j.get('month')==current and j.get('cache_hit') and j['status']=='done']
    folder=storage.DATA/'speech-cache'
    paths=list(folder.glob('*.mp3')) if folder.exists() else []
    return dict(month=current,success_estimated=used,uncertain_reserved=uncertain,
                protected_used=used+uncertain,limit=c['monthly_limit'],remaining=max(0,c['monthly_limit']-used-uncertain),
                requests=len(events),cache_hits=len(hits),cache_saved=sum(j.get('units',0) for j in hits),
                cache_files=len(paths),cache_bytes=sum(p.stat().st_size for p in paths if p.exists()),
                note='本机保守估算，汉字按双字符；失败或中断请求保留额度。未包含控制台或其他软件的调用，不等同于 Azure 账单。月份按 UTC。')


def voices(refresh=False):
    c=config()
    if not c['key']:
        raise ValueError('请先保存微软语音密钥。')
    ident=hashlib.sha256((resource_id(c)+c['key']).encode()).hexdigest()
    with VOICE_LOCK:
        cached=storage.get('speech_voices',ident)
        if cached and not refresh and time.time()-cached['created']<86400:
            return cached['voices']
        request=urllib.request.Request(endpoint(c)+'/cognitiveservices/voices/list',headers={
            'Ocp-Apim-Subscription-Key':storage.api_key(c),'User-Agent':'InterviewStudio/1.0'})
        try:
            with urllib.request.build_opener(NoRedirect).open(request,timeout=25) as response:
                rows=json.loads(response.read(2_000_000))
        except Exception:
            raise ValueError('读取微软音色列表失败，请检查密钥、区域和网络；未调用合成。') from None
        if not isinstance(rows,list):
            raise ValueError('微软音色列表格式异常。')
        result=[]
        for row in rows:
            name=row.get('ShortName')
            if row.get('VoiceType')=='Neural' and row.get('Status','GA')=='GA' and safe_voice(name):
                result.append(dict(id=name,name=row.get('LocalName') or row.get('DisplayName') or name,
                                   locale=row.get('Locale',''),gender=row.get('Gender','')))
        if not result:
            raise ValueError('当前区域未返回支持的普通 Neural 音色，未切换其他语音服务。')
        storage.put('speech_voices',ident,dict(created=time.time(),voices=result))
        return result


def cache_key(c,text,voice):
    return hashlib.sha256((resource_id(c)+'\0'+voice+'\0'+text+'\0mp3-v1').encode()).hexdigest()


def job_public(job):
    return {k:v for k,v in job.items() if k not in ('text','cache_key')}


def recover():
    for job in storage.all_records('speech_jobs'):
        if job['status'] in ('queued','running'):
            job.update(status='error',stage='error',finished=time.time(),error='本地服务重启，合成未确认完成；未自动重试。已发出的请求保留保护计数。')
            storage.put('speech_jobs',job['id'],job)


def submit(text,language,session_id=None,voice=None):
    c=config()
    voice=voice or c['voice_'+language]
    if not safe_voice(voice) or not voice.startswith(language+'-'):
        raise ValueError('请选择列表中对应语言的普通 Neural 音色。')
    key=cache_key(c,text,voice)
    cached=storage.DATA/'speech-cache'/(key+'.mp3')
    if not (cached.exists() and cached.stat().st_size):
        if not c['key']:
            raise ValueError('请先连接微软语音 API。')
        if voice not in {v['id'] for v in voices()}:
            raise ValueError('请选择微软列表中的普通 Neural 音色。')
    with LOCK:
        for existing in storage.all_records('speech_jobs'):
            if existing.get('cache_key')==key and existing['status'] in ('queued','running'):
                return dict(job_id=existing['id'])
        ident=uuid.uuid4().hex
        job=dict(id=ident,status='queued',stage='queued',created=time.time(),month=month(),resource=resource_id(c),
                 language=language,voice=voice,session_id=session_id,text=text,cache_key=key,
                 units=units(text),text_characters=len(text),cache_hit=False,received_bytes=0,total_bytes=None)
        storage.put('speech_jobs',ident,job)
        POOL.submit(run,ident,c)
    return dict(job_id=ident)


def run(ident,c):
    job=storage.get('speech_jobs',ident)
    folder=storage.DATA/'speech-cache';folder.mkdir(exist_ok=True)
    path=folder/(job['cache_key']+'.mp3')
    temp=folder/(ident+'.part')
    def update(**values):
        job.update(values);storage.put('speech_jobs',ident,job)
    try:
        update(status='running',stage='cache')
        if path.exists() and path.stat().st_size:
            update(status='done',stage='ready',cache_hit=True,finished=time.time(),received_bytes=path.stat().st_size,total_bytes=path.stat().st_size)
            return
        with LOCK:
            # Reserve before sending; a crash/timeout cannot silently reset quota.
            latest=config()
            if resource_id(latest)==resource_id(c):
                c['monthly_limit']=min(c['monthly_limit'],latest['monthly_limit'])
            stats=usage(c)
            if job['units']>stats['remaining']:
                raise ValueError('已达到本机月保护上限；可继续播放本地缓存。未切换收费服务。')
            recent=[e for e in storage.all_records('speech_events') if e.get('resource')==job['resource'] and time.time()-e['created']<60]
            if len(recent)>=18:
                raise ValueError('请求较密集，请稍后再次点击朗读；未自动重试。')
            job['month']=month()
            event=dict(id=ident,month=job['month'],resource=job['resource'],units=job['units'],created=time.time(),status='reserved')
            storage.put('speech_events',ident,event)
            update(stage='synthesis')
        locale='-'.join(job['voice'].split('-')[:2])
        ssml=f'<speak version="1.0" xml:lang="{locale}"><voice name="{job["voice"]}">{html.escape(job["text"],quote=False)}</voice></speak>'
        request=urllib.request.Request(endpoint(c)+'/cognitiveservices/v1',data=ssml.encode(),headers={
            'Ocp-Apim-Subscription-Key':storage.api_key(c),'Content-Type':'application/ssml+xml',
            'X-Microsoft-OutputFormat':'audio-24khz-48kbitrate-mono-mp3','User-Agent':'InterviewStudio/1.0'})
        with urllib.request.build_opener(NoRedirect).open(request,timeout=90) as response:
            if not response.headers.get('Content-Type','').lower().startswith('audio/'):
                raise ValueError('微软没有返回音频。未切换其他服务，保护计数已保留。')
            total=response.headers.get('Content-Length','')
            total=int(total) if total.isdigit() else None
            update(stage='download',total_bytes=total)
            received=0;last_write=0
            with temp.open('wb') as stream:
                while True:
                    block=response.read(16384)
                    if not block:break
                    received+=len(block)
                    if received>12_000_000:raise ValueError('音频超过处理上限；保护计数已保留。')
                    stream.write(block)
                    if time.monotonic()-last_write>.25:
                        update(received_bytes=received);last_write=time.monotonic()
            if not received or (total is not None and received!=total):
                raise ValueError('音频下载不完整，未自动重新合成。保护计数已保留。')
        with temp.open('rb') as stream:signature=stream.read(3)
        if not (signature==b'ID3' or (len(signature)>=2 and signature[0]==255 and signature[1]&224==224)):
            raise ValueError('收到的音频格式不正确，未自动重试。')
        temp.replace(path)
        event['status']='success';storage.put('speech_events',ident,event)
        update(status='done',stage='ready',finished=time.time(),received_bytes=received,total_bytes=received)
    except Exception as exc:
        if isinstance(exc,urllib.error.HTTPError):
            messages={401:'密钥或区域不正确',403:'免费额度或访问权限不可用',429:'微软限流或免费额度不足'}
            message=f'微软语音返回 {exc.code}：{messages.get(exc.code,"请求未完成")}。未自动重试或切换服务。'
        else:
            message=str(exc) if isinstance(exc,ValueError) else '语音连接中断或等待超时；已保留可能消耗的保护计数，未自动重试。'
        update(status='error',stage='error',finished=time.time(),error=message)
    finally:
        temp.unlink(missing_ok=True)


def audio_path(ident):
    job=storage.get('speech_jobs',ident)
    if not job or job['status']!='done':
        raise ValueError('音频还未准备好。')
    path=storage.DATA/'speech-cache'/(job['cache_key']+'.mp3')
    if not path.exists():
        raise ValueError('本地缓存文件不存在，请重新点击朗读。')
    return path
