import json
import os
import site
import threading
import subprocess
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOCK = threading.Lock()
MODEL = None
DEVICE = None
DLLS = []
TTS_LOCK = threading.Lock()

def synthesize(text, language):
    import storage
    ident = uuid.uuid4().hex
    input_path = storage.DATA / (ident + '.json')
    output_path = storage.DATA / (ident + '.wav')
    input_path.write_text(json.dumps(dict(text=text, language=language, output=str(output_path.resolve())),ensure_ascii=False),encoding='utf-8')
    try:
        with TTS_LOCK:
            result = subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'speak.ps1'),'-InputPath',str(input_path.resolve())],
                                    stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    creationflags=0x08000000,timeout=45)
        if result.returncode or not output_path.exists():
            raise ValueError('Windows 朗读未完成，请确认已安装对应语言的语音。')
        return output_path
    except Exception:
        output_path.unlink(missing_ok=True)
        raise
    finally:
        input_path.unlink(missing_ok=True)

def runtime():
    return json.loads((ROOT / 'runtime.json').read_text(encoding='utf-8'))

def available():
    return Path(runtime()['model_path'], 'model.bin').exists()

def transcribe(path, language, device):
    global MODEL, DEVICE
    with LOCK:
        from faster_whisper import WhisperModel
        if os.name == 'nt' and not DLLS:
            for folder in site.getsitepackages():
                for directory in (Path(folder) / 'nvidia').glob('*/bin'):
                    DLLS.append(os.add_dll_directory(str(directory)))
                    os.environ['PATH'] = str(directory) + os.pathsep + os.environ.get('PATH','')
        if not available():
            raise ValueError('本地语音模型不存在。请检查 runtime.json，或先用文字回答。')
        if MODEL is None or DEVICE != device:
            MODEL = None
            MODEL = WhisperModel(runtime()['model_path'], device=device,
                                 compute_type='float16' if device == 'cuda' else 'int8',
                                 local_files_only=True, cpu_threads=8)
            DEVICE = device
        segments, info = MODEL.transcribe(str(path), language=None if language == 'auto' else language,
                                          task='transcribe', vad_filter=True, beam_size=5,
                                          condition_on_previous_text=False)
        texts = [s.text.strip() for s in segments if not (s.no_speech_prob > .6 and s.avg_logprob < -.5)]
        text = ' '.join(texts).strip()
        if not text:
            raise ValueError('没有识别到清晰的人声。请重新录音，或直接输入回答。')
        return dict(text=text, language=info.language)
