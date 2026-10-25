import base64
import copy
import ctypes
import json
import os
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get('INTERVIEW_DATA_DIR', ROOT / 'data'))
DATA.mkdir(parents=True, exist_ok=True)
LOCK = threading.RLock()

@contextmanager
def db():
    connection = sqlite3.connect(DATA / 'interview.sqlite3', timeout=30)
    connection.execute('PRAGMA journal_mode=WAL')
    try:
        with connection:
            yield connection
    finally:
        connection.close()

with db() as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS records (kind TEXT, id TEXT, body TEXT, PRIMARY KEY(kind,id))')

def put(kind, key, value):
    with LOCK, db() as conn:
        conn.execute('INSERT OR REPLACE INTO records VALUES (?,?,?)', (kind, key, json.dumps(value, ensure_ascii=False)))

def get(kind, key, default=None):
    with LOCK, db() as conn:
        row = conn.execute('SELECT body FROM records WHERE kind=? AND id=?', (kind, key)).fetchone()
    return json.loads(row[0]) if row else default

def all_records(kind):
    with LOCK, db() as conn:
        rows = conn.execute('SELECT body FROM records WHERE kind=?', (kind,)).fetchall()
    return [json.loads(row[0]) for row in rows]

class Blob(ctypes.Structure):
    _fields_ = [('size', ctypes.c_ulong), ('data', ctypes.POINTER(ctypes.c_ubyte))]

def crypt(value, decrypt=False):
    if os.name != 'nt':
        raise ValueError('此版本使用 Windows 账户加密密钥。')
    buffer = ctypes.create_string_buffer(value)
    source = Blob(len(value), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)))
    result = Blob()
    fn = ctypes.windll.crypt32.CryptUnprotectData if decrypt else ctypes.windll.crypt32.CryptProtectData
    if not fn(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(result)):
        raise ValueError('无法读取本机加密密钥，请在设置中重新填写。')
    try:
        return ctypes.string_at(result.data, result.size)
    finally:
        ctypes.windll.kernel32.LocalFree(result.data)

DEFAULTS = {
    'subscription': {'name':'ChatGPT 订阅','base_url':'local-subscription','model':'','key':'','reasoning_effort':'low'},
    'deepseek': {'name':'DeepSeek','base_url':'https://api.deepseek.com','model':'','key':''},
    'zhipu': {'name':'智谱 GLM','base_url':'https://open.bigmodel.cn/api/paas/v4','model':'','key':''},
    'custom': {'name':'自定义服务','base_url':'','model':'','key':''},
}

def settings():
    config=get('settings', 'main', {'selected':'subscription','providers':copy.deepcopy(DEFAULTS),'device':'cuda','json_mode':True})
    for name,defaults in DEFAULTS.items():
        provider=config['providers'].setdefault(name,copy.deepcopy(defaults))
        for key,value in defaults.items():provider.setdefault(key,copy.deepcopy(value))
    return config

def public_settings():
    value = settings()
    for p in value['providers'].values():
        p['has_key'] = bool(p.pop('key', ''))
    return value

def api_key(provider):
    return crypt(base64.b64decode(provider['key']), True).decode() if provider.get('key') else ''

def save_settings(body):
    from urllib.parse import urlparse
    config = settings()
    selected = body.get('selected', config['selected'])
    if selected not in DEFAULTS:
        raise ValueError('请选择支持的服务。')
    provider = config['providers'][selected]
    if selected=='subscription':
        model=str(body.get('model',provider['model'])).strip()
        if not model or len(model)>200:raise ValueError('请检测并选择可用的订阅模型。')
        effort=body.get('reasoning_effort',provider.get('reasoning_effort','low'))
        if effort not in ('none','minimal','low','medium','high','xhigh','max'):
            raise ValueError('请选择有效的思考强度。')
        provider.update(model=model,base_url='local-subscription',key='',reasoning_effort=effort)
        config.update(selected=selected,device='cpu' if body.get('device')=='cpu' else 'cuda')
        put('settings','main',config)
        return public_settings()
    url = str(body.get('base_url', provider['base_url'])).strip().rstrip('/')
    parsed = urlparse(url)
    if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('请填写有效的 API 基础地址，不要在地址中放密钥。')
    if parsed.scheme == 'http' and parsed.hostname not in ('127.0.0.1','localhost','::1'):
        raise ValueError('远程服务请使用 HTTPS 地址。')
    model = str(body.get('model','')).strip()
    if not model or len(model) > 200:
        raise ValueError('请填写服务控制台显示的模型名称。')
    # Never carry credentials to a changed endpoint implicitly.
    if provider['base_url'] != url:
        provider['key'] = ''
    provider.update(base_url=url, model=model)
    key = str(body.get('api_key','')).strip()
    if body.get('clear_key'):
        provider['key'] = ''
    elif key:
        if len(key) > 4096:
            raise ValueError('密钥过长。')
        provider['key'] = base64.b64encode(crypt(key.encode())).decode()
    config['selected'] = selected
    config['json_mode'] = bool(body.get('json_mode', True))
    config['device'] = 'cpu' if body.get('device') == 'cpu' else 'cuda'
    put('settings', 'main', config)
    return public_settings()
