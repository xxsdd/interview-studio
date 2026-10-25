'use strict';
const discussionOpen = new Set();
let historyScroll = 0;
function correctAnswerHtml(feedback, english){
  if(!feedback.correct_answer)return bullets(feedback.improvements||[]);
  return '<div class="correct-answer"><p>'+e(feedback.correct_answer)+'</p><small>'+(english?'Reference answer, not your original response.':'参考回答，与上方你的回答分开。')+'</small></div>';
}
function renderHistoryPage(list=workspace.history){
  $('historyCount').textContent=list.length;
  const query=$('historySearch').value.trim().toLowerCase(),filter=$('historyFilter').value;
  const matches=list.filter(s=>s.title.toLowerCase().includes(query)&&(filter==='all'||s.status===filter));
  $('historyResultCount').textContent='共 '+list.length+' 场练习，当前显示 '+matches.length+' 场';
  $('history').innerHTML=matches.map(s=>`<article class="record-row"><div class="record-copy"><h2><button class="record-title" data-session="${e(s.id)}">${e(s.title)}</button></h2><p>${new Date(s.created*1000).toLocaleDateString()} · ${s.turns} 次回答</p></div><span class="record-state">${s.busy?'正在处理':s.status==='completed'?'已复盘':'练习中'}</span><div class="record-actions"><button class="quiet" data-session="${e(s.id)}">${s.status==='completed'?'查看记录':'查看 / 继续'}</button><button class="quiet danger-text" data-delete="${e(s.id)}" aria-label="删除练习 ${e(s.title)}" ${s.busy?'disabled':''}>删除</button></div></article>`).join('')||'<p class="empty-state">'+(list.length?'没有匹配的记录，请换个关键词或状态。':'还没有练习记录，从“新的练习”开始吧。')+'</p>';
  $('history').querySelectorAll('[data-session]').forEach(b=>b.onclick=()=>loadSession(b.dataset.session).catch(err=>notice(err.message,true)));
  $('history').querySelectorAll('[data-delete]').forEach(b=>b.onclick=()=>deletePractice(b.dataset.delete));
}
function closeHistoryPage(){
  document.body.classList.remove('history-view');$('historyPage').hidden=true;
  $('historyOpen').removeAttribute('aria-current');
}
function openHistoryPage(){
  if(state.recorder||state.asrBusy){notice('请先完成或放弃当前录音。',true);return;}
  historyScroll=window.scrollY;stopSpeaking();document.body.classList.add('history-view');
  $('historyPage').hidden=false;$('historyOpen').setAttribute('aria-current','page');
  workspaceView();renderHistoryPage();window.scrollTo(0,0);$('historyTitle').focus();
  refreshHistory().catch(err=>notice(err.message,true));
}
$('historyOpen').onclick=openHistoryPage;
$('historyBack').onclick=()=>{closeHistoryPage();workspaceView();window.scrollTo(0,historyScroll);$('historyOpen').focus({preventScroll:true});};
$('historySearch').oninput=()=>renderHistoryPage();
$('historyFilter').onchange=()=>renderHistoryPage();
function discussionKey(turnId){return 'discussion-draft-'+state.session.id+'-'+turnId;}
function discussionHtml(turn){
  const entries=turn.clarifications||[],open=discussionOpen.has(turn.id)||entries.length;
  return `<details class="feedback-discussion" id="discussion-${e(turn.id)}" data-discussion="${e(turn.id)}" ${open?'open':''}><summary>没听懂？继续提问${entries.length?'（'+entries.length+'）':''}</summary><p class="hint">围绕这道题和反馈继续问。讨论不会计入答题数，也不改变考点进度。</p><div class="discussion-messages">${entries.map(c=>`<section class="discussion-exchange"><p class="discussion-question"><b>你的提问</b><br>${e(c.question)}</p>${c.answer?'<div class="discussion-explanation"><b>解释</b><p>'+e(c.answer)+'</p></div>'+usageHtml(c.usage):'<p class="hint">解释尚未完成，请查看下方处理状态；不会自动重新调用 AI。</p>'}</section>`).join('')}</div><form class="discussion-form" data-turn="${e(turn.id)}"><label for="ask-${e(turn.id)}">你想进一步了解什么？</label><textarea id="ask-${e(turn.id)}" rows="3" maxlength="12000" required placeholder="例如：为什么要这样做？能用一个具体例子解释吗？" ${state.session.busy?'disabled':''}>${e(localStorage.getItem(discussionKey(turn.id))||'')}</textarea><div class="discussion-actions"><span class="hint">使用当前所选模型与思考强度</span><button type="submit" class="primary" ${state.session.busy?'disabled':''}>发送提问</button></div><p class="discussion-error" role="status" hidden></p></form></details>`;
}
function bindDiscussions(){
  $('conversation').querySelectorAll('[data-discussion]').forEach(d=>d.ontoggle=()=>{if(d.open)discussionOpen.add(d.dataset.discussion);else discussionOpen.delete(d.dataset.discussion);});
  $('conversation').querySelectorAll('.discussion-form').forEach(form=>{
    const input=form.querySelector('textarea'),button=form.querySelector('button'),error=form.querySelector('.discussion-error');
    input.oninput=()=>localStorage.setItem(discussionKey(form.dataset.turn),input.value);
    form.onsubmit=async event=>{
      event.preventDefault();
      if(state.session.busy||state.recorder||state.asrBusy){error.hidden=false;error.textContent='请先完成当前处理或录音。';return;}
      const text=input.value.trim();if(!text){input.focus();return;}
      const sid=state.session.id,key=discussionKey(form.dataset.turn);
      button.disabled=true;error.hidden=true;discussionOpen.add(form.dataset.turn);
      // Reuse the ID after a network failure, so a lost response cannot duplicate a charge.
      const requestKey=key+'-request';let request;
      try{request=JSON.parse(localStorage.getItem(requestKey)||'null');}catch{}
      if(!request||request.text!==text)request={text,id:crypto.randomUUID()};
      localStorage.setItem(requestKey,JSON.stringify(request));
      try{
        const out=await api('/api/sessions/'+sid+'/clarify',{request_id:request.id,turn_id:form.dataset.turn,text});
        const updated=await api('/api/sessions/'+sid);
        localStorage.removeItem(key);stopSpeaking();
        if(state.session?.id===sid){state.session=updated;await renderSession();}
        localStorage.removeItem(requestKey);
        pollTask(out.task_id,sid);
      }catch(err){error.hidden=false;error.textContent=err.message;button.disabled=false;}
    };
  });
}
