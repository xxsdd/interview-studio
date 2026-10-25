'use strict';
let modelVersion=0, modelTimer=null, progressTask=null;
const numberText=v=>Number.isInteger(v)&&v>=0?v.toLocaleString():'—';
function usageValues(raw={}){return {input:raw.prompt_tokens??raw.input_tokens??null,output:raw.completion_tokens??raw.output_tokens??null,total:raw.total_tokens??null};}
function usageText(raw={}){const v=usageValues(raw);return `输入 ${numberText(v.input)} · 输出 ${numberText(v.output)} Token`;}
function usageHtml(raw={}){const v=usageValues(raw);return `<p class="turn-usage">${e(usageText(raw))}<span>${v.input===null||v.output===null?'服务未返回完整用量':'服务返回的实际用量'}</span></p>`;}
function renderUsage(summary){
  $('usagePanel').hidden=!state.session;
  if(!summary){$('usagePanel').textContent='本场 Token 用量：等待服务返回';return;}
  const values=summary.totals;
  function count(key){const value=values[key];return (value!==null&&summary.missing[key]>0?'≥ ':'')+numberText(value);}
  $('usagePanel').innerHTML=`<div class="usage-title">本场 Token</div><div><small>输入</small><strong>${count('input')}</strong></div><div><small>输出</small><strong>${count('output')}</strong></div><div><small>合计</small><strong>${count('total')}</strong></div><details><summary>统计说明</summary><p>统计 ${summary.requests} 次请求，包括首题、回答、复盘和重试。输出数可能包含模型思考用量，以服务口径为准。${summary.pending?' 当前有请求尚未结束。':''}${Object.values(summary.missing).some(v=>v>0)?' 部分请求未返回完整用量，缺失值不按零计算，“≥”表示已知小计。':''}</p></details>`;
}
function renderProgress(task){
  progressTask=task;
  const box=$('taskProgress');
  if(!task){box.hidden=true;return;}
  box.hidden=false;
  const p=task.progress;
  const active=['pending','running'].includes(task.status);
  const title=({start:'面试官的问题',answer:'回答反馈与下一道问题',summary:'本场面试复盘',clarify:'解释你的疑问'})[task.action]||'处理中';
  const elapsed=Math.max(0,Math.floor((task.finished||Date.now()/1000)-task.created));
  const tokens=task.tokens||{input:null,output:null,total:null};
  const tokenLine=`输入 ${numberText(tokens.input)} · 输出 ${numberText(tokens.output)} Token`;
  box.className='task-progress '+(active?'is-running':task.status==='error'?'is-error':'is-done');
  box.innerHTML=`<div class="progress-heading"><strong>${e(title)}</strong><span>${task.status==='done'?'已完成':task.status==='error'?'已停止':`已等待 ${elapsed} 秒`}</span></div>${p?`<progress value="${p.completed}" max="${p.total}" aria-label="已完成处理步骤">${p.completed}/${p.total}</progress><div class="progress-steps">${p.steps.map(s=>`<span class="${s.done?'complete':s.id===p.stage&&active?'current':''}">${s.done?'✓ ':''}${e(s.label)}</span>`).join('')}</div><p class="progress-detail">${task.status==='error'?'处理未完成，已保存当前记录':e(p.detail)}${active&&p.received_chars?` · 已接收 ${p.received_chars.toLocaleString()} 字符（不是 Token）`:''}${active?' · 按实际处理步骤推进，不代表剩余时间':''}</p>`:''}<div class="progress-tokens">${e(tokenLine)}<small>${active&&tokens.input===null?'准确用量等待服务返回':tokens.input===null||tokens.output===null?'服务未返回完整 Token 用量':'包含本次请求的实际用量'}</small></div>${task.provider_name==='ChatGPT 订阅'?'<p class="hint">ChatGPT 订阅额度 · 不固定限制 3,000 Token · 异常输出自动中断</p>':''}${task.output_limit?`<p class="hint">单次输出上限 ${numberText(task.output_limit)} Token（输入另计）</p>`:""}${active?`<button class="quiet danger-text" id="stopGeneration" ${task.cancel_requested?"disabled":""}>${task.cancel_requested?"正在停止…":"停止生成"}</button>`:""}`;
  if(!active&&task.status==='done')box.innerHTML='<details class="completed-task"><summary>本轮处理已完成 · '+e(tokenLine)+'</summary>'+box.innerHTML+'</details>';
  $("stopGeneration")?.addEventListener("click",async()=>{task.cancel_requested=true;renderProgress(task);try{await api("/api/tasks/"+task.id+"/cancel",{});}catch(err){task.cancel_requested=false;renderProgress(task);notice(err.message,true);}});
}
setInterval(()=>{if(progressTask&&['pending','running'].includes(progressTask.status)&&!$('taskProgress').hidden)renderProgress(progressTask);},1000);

function modelSelection(){const value=$('modelSelect').value;const manual=value==='__manual__';$('model').hidden=!manual;$('model').required=manual;if(!manual)$('model').value=value;window.syncSettingsReasoning?.();}
function modelOptions(models=[],source='api'){
  if(source==='subscription'&&window.syncSettingsReasoning)modelChoice.models=models;
  const current=$('model').value.trim()||(source==='subscription'?(models.find(m=>m.default)?.id||models[0]?.id||''):'');
  const ids=models.map(m=>m.id);
  let html='<option value="">请选择模型</option>';
  if(current&&!ids.includes(current))html+=`<option value="${e(current)}">${e(current)}（当前填写）</option>`;
  html+=models.map(m=>`<option value="${e(m.id)}">${e(m.id)}${source==='reference'?'（待验证）':''}</option>`).join('');
  html+='<option value="__manual__">手动填写其他模型…</option>';
  $('modelSelect').innerHTML=html;
  $('modelSelect').value=current||(!models.length?'__manual__':'');
  modelSelection();
}
function resetModelDiscovery(){clearTimeout(modelTimer);modelVersion++;$('detectModels').disabled=false;modelOptions();$('modelStatus').textContent='输入密钥后自动读取模型列表，不会发送生成请求。';queueDiscovery(250);}
function queueDiscovery(delay=900){
  clearTimeout(modelTimer);modelVersion++;
  $('detectModels').disabled=false;
  $('modelStatus').textContent='输入密钥后自动读取模型列表，不会发送生成请求。';
  const selected=$('provider').value,p=state.settings.providers[selected];
  const typed=$('apiKey').value.trim();
  const stored=p.has_key&&$('baseUrl').value.trim().replace(/\/$/,'')===p.base_url&&!$('clearKey').checked;
  if((typed.length>=12||(!typed&&stored)||['custom','subscription'].includes(selected))&&!$('clearKey').checked){modelTimer=setTimeout(()=>discoverModels(),delay);}
}
async function discoverModels(){
  clearTimeout(modelTimer);
  const version=++modelVersion;
  const body={selected:$('provider').value,base_url:$('baseUrl').value,api_key:$('apiKey').value,clear_key:$('clearKey').checked};
  $('detectModels').disabled=true;$('modelStatus').textContent='正在读取服务返回的模型列表…';
  try{
    const result=await api('/api/models/discover',body);
    if(version!==modelVersion)return;
    modelOptions(result.models,result.source);$('modelStatus').textContent=result.message;
  }catch(err){if(version!==modelVersion)return;$('modelStatus').textContent=err.message;}
  finally{if(version===modelVersion)$('detectModels').disabled=false;}
}
$('modelSelect').onchange=modelSelection;
$('detectModels').onclick=discoverModels;
$('apiKey').addEventListener('input',()=>{modelOptions();queueDiscovery();});
$('baseUrl').addEventListener('input',()=>{modelOptions();queueDiscovery();});
$('clearKey').addEventListener('change',()=>{queueDiscovery();if($('clearKey').checked)$('modelStatus').textContent='已选择清除密钥；取消勾选后可继续检测。';});
$('settingsDialog').addEventListener('close',()=>{clearTimeout(modelTimer);modelVersion++;$('detectModels').disabled=false;});

async function refreshTrash(){const list=await api('/api/trash');$('trashCount').textContent=list.length;return list;}
async function deletePractice(id){
  if(id===state.session?.id&&(state.recorder||state.asrBusy)){notice('请先结束录音和转写，再删除本场。',true);return;}
  const fromHistory=document.body.classList.contains('history-view');
  try{await api('/api/sessions/'+id+'/trash',{});if(state.session?.id===id)await newSession();if(fromHistory)openHistoryPage();await refreshHistory();notice('练习已移到“最近删除”，需要时可以恢复。');}catch(err){notice(err.message,true);}
}
async function showTrash(){
  const list=await refreshTrash();
  $('trashList').innerHTML=list.length?list.map(s=>`<div class="trash-item"><div><strong>${e(s.title)}</strong><small>${new Date(s.created*1000).toLocaleString()} · ${s.turns} 次回答</small></div><button class="quiet" data-restore="${e(s.id)}">恢复</button></div>`).join(''):'<p class="muted">没有已删除的练习。</p>';
  $('trashList').querySelectorAll('[data-restore]').forEach(button=>button.onclick=async()=>{try{button.disabled=true;await api('/api/sessions/'+button.dataset.restore+'/restore',{});await refreshHistory();await showTrash();}catch(err){notice(err.message,true);button.disabled=false;}});
  if(!$('trashDialog').open)$('trashDialog').showModal();
}
$('trashOpen').onclick=()=>showTrash().catch(err=>notice(err.message,true));
$('deleteCurrent').onclick=()=>state.session&&deletePractice(state.session.id);
