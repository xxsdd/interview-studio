"""Launch the local server in the background and open its browser UI."""
import ctypes
import json
import os
import subprocess
import sys
import time
import traceback
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URL = 'http://127.0.0.1:8766'

def running():
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(URL+'/api/health',timeout=2) as response:
            return json.load(response).get('app')=='interview-studio'
    except Exception:
        return False

def main():
    if not running():
        runtime=json.loads((ROOT/'runtime.json').read_text(encoding='utf-8'))
        (ROOT/'data').mkdir(exist_ok=True)
        with (ROOT/'data'/'server.log').open('a',encoding='utf-8') as log:
            process=subprocess.Popen([runtime['python'],'-m','uvicorn','app:app','--host','127.0.0.1','--port','8766','--no-access-log'],cwd=ROOT,
                                     env={**os.environ,'PYTHONUTF8':'1','HF_HUB_OFFLINE':'1'},stdout=log,stderr=log,stdin=subprocess.DEVNULL,
                                     creationflags=0x08000000 if os.name=='nt' else 0)
            (ROOT/'data'/'server.pid').write_text(str(process.pid))
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            if running():break
            if process.poll() is not None:
                raise RuntimeError('后台服务已退出，请查看 data/server.log。')
            time.sleep(.25)
    if running():
        if '--no-browser' not in sys.argv:
            if os.name=='nt':
                os.startfile(URL)
            elif not webbrowser.open(URL):
                raise RuntimeError('无法打开默认浏览器，请手动访问 ' + URL)
        if sys.stdout: print(URL)
    else:
        raise RuntimeError('答练在 60 秒内未能启动。请检查 data/server.log，确认 runtime.json 指向有效的 Python 环境。')

if __name__=='__main__':
    try:
        (ROOT/'data').mkdir(exist_ok=True)
        with (ROOT/'data'/'launcher.log').open('a',encoding='utf-8') as log:
            log.write('\n' + time.strftime('%Y-%m-%d %H:%M:%S') + ' START ' + sys.executable + '\n')
        main()
        with (ROOT/'data'/'launcher.log').open('a',encoding='utf-8') as log:
            log.write(time.strftime('%Y-%m-%d %H:%M:%S') + ' READY ' + URL + '\n')
    except Exception as exc:
        (ROOT/'data').mkdir(exist_ok=True)
        with (ROOT/'data'/'launcher.log').open('a',encoding='utf-8') as log:
            log.write('\n' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
            traceback.print_exc(file=log)
        message = f'答练启动失败：{exc}\n\n详细日志：{ROOT / "data" / "launcher.log"}'
        if os.name=='nt':ctypes.windll.user32.MessageBoxW(0,message,'答练',0x10)
        elif sys.stderr: print(message,file=sys.stderr)
        raise SystemExit(1)
