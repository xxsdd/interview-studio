'use strict';
let speechSequence=0, audioUrl=null, speechJob=null, speechStarted=0;
let speechConfig=null, speechVoices=[], speechStats=null;
const speedOptions=[.5,.75,1,1.25,1.5,1.75,2];
function autoReadEnabled(){return localStorage.getItem('interview-auto-read')==='true';}
$('autoReadQuestions').checked=autoReadEnabled();
$('autoReadQuestions').onchange=()=>{localStorage.setItem('interview-auto-read',String($('autoReadQuestions').checked));if(!$('autoReadQuestions').checked)stopSpeaking();};
let playbackSpeed=Number(localStorage.getItem('interview-speech-speed')||1);
if(!speedOptions.includes(playbackSpeed))playbackSpeed=1;
for(const id of ['playbackRate','settingsPlaybackRate']){
  $(id).innerHTML=speedOptions.map(v=>`<option value="${v}">${v}×${v===1?' 正常':''}</option>`).join('');
  $(id).value=String(playbackSpeed);
  $(id).onchange=()=>setPlaybackSpeed(Number($(id).value));
}
function setPlaybackSpeed(speed){
  playbackSpeed=speed;localStorage.setItem('interview-speech-speed',String(speed));
  for(const id of ['playbackRate','settingsPlaybackRate'])$(id).value=String(speed);
  $('questionAudio').playbackRate=speed;$('questionAudio').preservesPitch=true;
}
function stopSpeaking(){
  speechSequence++;speechJob=null;window.speechSynthesis?.cancel();
  $('questionAudio').pause();$('questionAudio').hidden=true;
  if(audioUrl){URL.revokeObjectURL(audioUrl);audioUrl=null;}
  if(!$('speechPlayer').hidden)$('speechLoadLabel').textContent='已停止。已发出的合成请求会继续存入本机缓存。';
  $('speechPreviewStatus').textContent='已停止。已发出的合成请求仍会缓存。';
  $('speechLoadProgress').value=0;
}
function renderSpeechUsage(){
  if(!speechStats)return;
  const u=speechStats;
  $('speechUsageStrip').hidden=!speechConfig?.has_key;
  const line=`语音 · ${u.month}（UTC） · 合成估算 ${numberText(u.success_estimated)} 字符单位${u.uncertain_reserved?` · 待确认 ${numberText(u.uncertain_reserved)}`:''} · 缓存命中 ${u.cache_hits} 次`;
  $('speechUsageText').textContent=line;
  $('speechUsageDetails').innerHTML=`<div class="speech-usage-grid"><div><small>成功合成估算</small><strong>${numberText(u.success_estimated)}</strong></div><div><small>失败 / 未确认占用</small><strong>${numberText(u.uncertain_reserved)}</strong></div><div><small>保护上限</small><strong>${numberText(u.limit)}</strong></div><div><small>可用保护额度</small><strong>${numberText(u.remaining)}</strong></div></div><p class="hint">${u.requests} 次云端请求 · ${u.cache_hits} 次命中本机缓存 · 约省 ${numberText(u.cache_saved)} 字符单位<br>本机缓存 ${u.cache_files} 段，${(u.cache_bytes/1048576).toFixed(2)} MB。改变倍速不重新合成。</p><p class="hint">${e(u.note)}</p>`;
}
async function refreshSpeech(){const data=await api('/api/speech/settings');speechConfig=data.settings;speechStats=data.usage;renderSpeechUsage();return data;}
function fillSpeechSettings(){
  const c=speechConfig;
  $('autoReadQuestions').checked=autoReadEnabled();
  $('speechRegion').value=c.region;$('speechResource').value=c.resource;$('speechKey').value='';$('speechClearKey').checked=false;
  $('speechKeyStatus').textContent=c.has_key?'已加密保存，可直接使用':'尚未连接';
  $('speechLimit').value=c.monthly_limit;
  $('voiceZh').value=c.voice_zh;$('voiceEn').value=c.voice_en;
  updateVoiceChoices();
}
function updateVoiceChoices(){
  for(const lang of ['zh','en']){
    const select=$('voice'+(lang==='zh'?'Zh':'En'));
    const current=select.value||speechConfig['voice_'+lang];
    const options=speechVoices.filter(v=>v.id.startsWith(lang+'-'));
    const listed=options.some(v=>v.id===current);
    select.innerHTML=(!listed?`<option value="${e(current)}">${e(current)}（当前选择）</option>`:'')+options.map(v=>`<option value="${e(v.id)}">${e(v.name)} · ${e(v.locale)} · ${v.gender==='Female'?'女声':'男声'}</option>`).join('');
    select.value=current;
  }
}
async function loadSpeechVoices(refresh=false){
  $('speechVoicesStatus').textContent='正在读取普通 Neural 音色列表…';$('refreshSpeechVoices').disabled=true;
  try{const data=await api('/api/speech/voices',{refresh});speechVoices=data.voices;updateVoiceChoices();$('speechVoicesStatus').textContent=`可选 ${speechVoices.length} 个普通 Neural 音色。仅试听或朗读时消耗合成字符；试听也会缓存。`;}
  catch(err){$('speechVoicesStatus').textContent=err.message;}
  finally{$('refreshSpeechVoices').disabled=false;}
}
async function openSpeechSettings(){
  try{await refreshSpeech();fillSpeechSettings();$('speechSettingsError').textContent='';$('speechSettingsDialog').showModal();if(speechConfig.has_key)await loadSpeechVoices();}
  catch(err){notice(err.message,true);}
}
$('speechSettingsOpen').onclick=openSpeechSettings;$('speechUsageOpen').onclick=openSpeechSettings;
$('refreshSpeechUsage').onclick=()=>refreshSpeech().catch(err=>notice(err.message,true));
$('refreshSpeechVoices').onclick=()=>loadSpeechVoices(true);
$('speechSettingsForm').onsubmit=async event=>{
  event.preventDefault();$('saveSpeechSettings').disabled=true;$('speechSettingsError').textContent='';
  try{
    const data=await api('/api/speech/settings',{region:$('speechRegion').value,resource:$('speechResource').value,
      api_key:$('speechKey').value,clear_key:$('speechClearKey').checked,
      voice_zh:$('voiceZh').value,voice_en:$('voiceEn').value,monthly_limit:Number($('speechLimit').value)});
    speechConfig=data.settings;speechStats=data.usage;$('speechKey').value='';$('speechClearKey').checked=false;
    $('speechKeyStatus').textContent=speechConfig.has_key?'已加密保存，可直接使用':'尚未连接';renderSpeechUsage();
    $('speechSettingsError').textContent='已保存。音频保存在本机缓存，倍速在本机调整。';
    if(speechConfig.has_key)await loadSpeechVoices();
  }catch(err){$('speechSettingsError').textContent=err.message;}
  finally{$('saveSpeechSettings').disabled=false;}
};
$('speechSettingsDialog').addEventListener('close',()=>{$('speechKey').value='';if($('questionAudio').parentElement===$('speechPreviewPlayer'))stopSpeaking();});
function showSpeechProgress(job){
  const labels={queued:'等待合成',cache:'检查本机缓存',synthesis:'微软正在合成问题语音',download:'下载音频到本机',ready:'语音已就绪',error:'语音未完成'};
  const elapsed=Math.max(0,Math.floor(Date.now()/1000-(job.created||speechStarted)));
  $('speechPlayer').hidden=false;
  $('speechLoadLabel').textContent=job.status==='done'?(job.cache_hit?'来自本机缓存 · 本次新增消耗 0':`已缓存到本机 · 本次估算 ${job.units} 字符单位`):job.status==='error'?job.error:`${labels[job.stage]||'正在准备'} · ${elapsed} 秒`;
  const progress=$('speechLoadProgress');
  if(job.status==='done'){progress.value=100;}
  else if(job.status==='error'){progress.value=0;}
  else if(job.stage==='download'&&job.total_bytes){progress.value=Math.floor(job.received_bytes/job.total_bytes*100);}
  else{progress.removeAttribute('value');}
  $('speechLoadDetail').textContent=job.stage==='download'?`已接收 ${(job.received_bytes/1024).toFixed(1)} KB${job.total_bytes?` / ${(job.total_bytes/1024).toFixed(1)} KB`:''}`:job.status==='done'?`${job.voice} · 音频仅存本机`:'合成等待期间显示动态进度，收到音频后按下载量更新。';
  $('speechPreviewStatus').textContent=$('speechLoadLabel').textContent;
  if(progress.hasAttribute('value'))$('speechPreviewProgress').value=progress.value;
  else $('speechPreviewProgress').removeAttribute('value');
}
setInterval(()=>{if(speechJob&&['queued','running'].includes(speechJob.status))showSpeechProgress(speechJob);},1000);
async function playQuestion(body){
  stopSpeaking();const sequence=speechSequence;speechStarted=Date.now()/1000;
  $('speechPreviewPlayer').hidden=!body.preview;
  (body.preview?$('speechPreviewPlayer'):$('speechPlayer')).appendChild($('questionAudio'));
  $('speechQuestionText').textContent=body.preview?'音色试听':body.text;
  speechJob={status:'queued',stage:'cache',created:speechStarted};showSpeechProgress(speechJob);
  try{
    const out=await api('/api/speech/jobs',body);
    if(!body.preview&&sequence===speechSequence)$('speechPlayer').scrollIntoView({behavior:'smooth',block:'center'});
    let job;
    do{
      job=await api('/api/speech/jobs/'+out.job_id);
      if(sequence!==speechSequence)return;
      speechJob=job;showSpeechProgress(job);
      if(['queued','running'].includes(job.status))await new Promise(resolve=>setTimeout(resolve,450));
    }while(['queued','running'].includes(job.status));
    await refreshSpeech();
    if(job.status==='error')throw Error(job.error);
    if(sequence!==speechSequence)return;
    const response=await fetch('/api/speech/audio/'+out.job_id);
    if(!response.ok)throw Error('读取本机音频缓存失败，请再次点击朗读。');
    const blob=await response.blob();
    if(sequence!==speechSequence)return;
    audioUrl=URL.createObjectURL(blob);$('questionAudio').src=audioUrl;$('questionAudio').hidden=false;
    setPlaybackSpeed(playbackSpeed);
    try{await $('questionAudio').play();}catch(err){$('speechLoadLabel').textContent+=' · 点击播放器开始播放';}
  }catch(err){
    if(sequence===speechSequence){speechJob=null;$('speechLoadProgress').value=0;$('speechLoadLabel').textContent=err.message;$('speechLoadDetail').textContent='未自动重试或切换服务。';$('speechPreviewStatus').textContent=err.message;$('speechPreviewProgress').value=0;}
    refreshSpeech().catch(()=>{});
  }
}
async function speak(text,language){
  if(!state.session)return;
  return playQuestion({session_id:state.session.id,text,language});
}
$('previewZh').onclick=()=>playQuestion({preview:true,language:'zh',voice:$('voiceZh').value});
$('previewEn').onclick=()=>playQuestion({preview:true,language:'en',voice:$('voiceEn').value});
$('stopQuestionAudio').onclick=stopSpeaking;
$('stopPreviewAudio').onclick=stopSpeaking;
$('questionAudio').addEventListener('error',()=>{$('speechLoadLabel').textContent='音频播放失败，可再次点击朗读读取本机缓存。';$('speechPreviewStatus').textContent=$('speechLoadLabel').textContent;});
window.addEventListener('DOMContentLoaded',()=>refreshSpeech().catch(()=>{}));
