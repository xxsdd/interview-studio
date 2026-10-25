'use strict';
// One manually selected subscription model per request. No automatic routing.
const modelChoice={models:null,loading:false,saving:false,error:''};
const practiceModels=[{id:'gpt-6-luna',label:'Luna'},{id:'gpt-6.1-sol',label:'Sol · GPT-6.1'},{id:'gpt-6-astra',label:'Astra'}];
const effortLabels={none:'不启用思考 · none',minimal:'最少 · minimal',low:'低 · low',medium:'中 · medium',high:'高 · high',xhigh:'更高 · xhigh',max:'最高 · max'};
function reasoningOptions(select,modelId,current){
  const model=modelChoice.models?.find(m=>m.id===modelId);
  const choices=(model?.reasoning_efforts||[]).filter(v=>Object.hasOwn(effortLabels,v));
  const options=choices.map(v=>`<option value="${v}">${effortLabels[v]}</option>`).join('');
  select.innerHTML=options||'<option value="">先检测模型</option>';
  select.value=choices.includes(current)?current:choices.includes('low')?'low':choices.includes(model?.default_effort)?model.default_effort:choices[0]||'';
  return choices.length>0;
}
function syncSettingsReasoning(){
  const sub=$('provider').value==='subscription';$('settingsReasoningRow').hidden=!sub;
  if(!sub)return;
  const current=$('settingsReasoning').value||state.settings.providers.subscription.reasoning_effort||'low';
  $('settingsReasoning').disabled=!reasoningOptions($('settingsReasoning'),$('model').value,current);
}
function refreshModelChoice(){
  const subscription=state.settings?.selected==='subscription';
  $('modelChoiceBar').hidden=!subscription;if(!subscription)return;
  const current=state.settings.providers.subscription.model;
  const select=$('practiceModel');const busy=!!state.session?.busy;
  const available=modelChoice.models?new Set(modelChoice.models.map(m=>m.id)):new Set([current]);
  const choices=practiceModels.filter(m=>available.has(m.id));
  if(current&&!choices.some(m=>m.id===current))choices.push({id:current,label:current+(modelChoice.models&&!available.has(current)?'（当前未列出）':'')});
  const options=choices.map(m=>`<option value="${e(m.id)}">${e(m.label)}</option>`).join('');if(select.innerHTML!==options)select.innerHTML=options;
  select.value=current;select.disabled=busy||modelChoice.loading||modelChoice.saving||!modelChoice.models;
  const validEffort=reasoningOptions($('practiceReasoning'),current,state.settings.providers.subscription.reasoning_effort||'low');
  $('practiceReasoning').disabled=busy||modelChoice.loading||modelChoice.saving||!validEffort;
  $('refreshPracticeModels').disabled=modelChoice.loading||modelChoice.saving||busy;
  $('practiceModelStatus').textContent=modelChoice.error||(modelChoice.loading?'正在检测模型与思考档位，不会生成内容…':modelChoice.saving?'正在保存…':busy?'本轮保持原设置，处理完成后可切换。':'选择自动保存在本机 · 下一次请求生效 · 较高强度可能增加等待和用量');
  if(!modelChoice.models&&!modelChoice.loading&&!modelChoice.error)loadPracticeModels();
}
async function loadPracticeModels(){
  if(modelChoice.loading)return;modelChoice.loading=true;modelChoice.error='';refreshModelChoice();
  try{const result=await api('/api/subscription/status');modelChoice.models=result.models||[];syncSettingsReasoning();}
  catch(err){modelChoice.error='检测未完成：'+err.message;}
  finally{modelChoice.loading=false;refreshModelChoice();}
}
$('refreshPracticeModels').onclick=loadPracticeModels;
async function savePracticeChoice(){
  const model=$('practiceModel').value;if(!modelChoice.models?.some(m=>m.id===model))return;
  const reasoning_effort=$('practiceReasoning').value;if(!reasoning_effort)return;
  modelChoice.saving=true;modelChoice.error='';refreshModelChoice();
  try{state.settings=await api('/api/settings',{selected:'subscription',model,reasoning_effort,device:state.settings.device});updateConnection();notice('已保存 '+(practiceModels.find(m=>m.id===model)?.label||model)+' · 思考强度 '+effortLabels[reasoning_effort]+'，下一次请求生效。');}
  catch(err){modelChoice.error=err.message;notice('模型未切换：'+err.message,true);}
  finally{modelChoice.saving=false;refreshModelChoice();}
}
$('practiceModel').onchange=()=>{reasoningOptions($('practiceReasoning'),$('practiceModel').value,state.settings.providers.subscription.reasoning_effort||'low');savePracticeChoice();};
$('practiceReasoning').onchange=savePracticeChoice;
