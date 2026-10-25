'use strict';
let libraryData=null, lessonDetail=null, lessonRequest=0;
const pointLabel=p=>p?.status==='passed'?'已通过':p?.attempts?'待巩固':'未考查';
function coverageHtml(plan,progress){
  if(!plan)return '<p class="hint">开始练习时，AI 会依据原文建立考点清单；之后复用本机清单。</p>';
  const item=p=>{const v=progress?.points?.[p.id];return `<li><div><strong>${e(p.title)}</strong><span class="point-status ${v?.status==='passed'?'passed':v?.attempts?'review':''}">${pointLabel(v)}</span></div><p>${e(p.criteria)}</p>${v?.reason?`<small>${e(v.reason)}</small>`:''}</li>`;};
  const groups=['理解原理','选择方案','排查问题','项目应用','其他考点'].map(skill=>({skill,points:plan.points.filter(p=>(['理解原理','选择方案','排查问题','项目应用'].includes(p.skill)?p.skill:'其他考点')===skill)})).filter(g=>g.points.length);
  return `${plan.coverage_notes?.length?`<p class="hint">${plan.coverage_notes.map(e).join('<br>')}</p>`:''}${groups.map(g=>`<details class="coverage-group"><summary>${g.skill} · ${g.points.filter(p=>progress?.points?.[p.id]?.status==='passed').length}/${g.points.length} 通过</summary><ol class="coverage-list">${g.points.map(item).join('')}</ol></details>`).join('')}`;
}
function studyModeChanged(){const studyMode=$('practiceType').value==='study';$('librarySetup').hidden=!studyMode;$('bankSetup').hidden=studyMode;document.body.dataset.practiceMode=studyMode?'study':'interview';$('startSession').innerHTML=studyMode?'开始／继续练习 <span>↗</span>':'开始面试 <span>↗</span>';localStorage.setItem('practice-type',$('practiceType').value);if(!studyMode)$('startSession').disabled=false;else $('startSession').disabled=!lessonDetail;if(libraryData)renderWorkspaceHome();}
async function initLibrary(){
  libraryData=await api('/api/library');
  $('libraryCount').textContent=`三周计划 · ${libraryData.units.filter(u=>u.full_article).length} 篇完整文章；另保留原有 ${libraryData.documents} 份教材资料。`;
  $('bookSelect').innerHTML=libraryData.books.map(b=>`<option value="${b.id}">${e(b.title)}</option>`).join('');
  const saved=localStorage.getItem('article-view-v2')?JSON.parse(localStorage.getItem('study-selection')||'{}'):{book:'plan'};
  localStorage.setItem('article-view-v2','1');
  if(libraryData.books.some(b=>b.id===saved.book))$('bookSelect').value=saved.book;
  $('practiceType').value=localStorage.getItem('practice-type')||'study';
  $('practiceType').onchange=studyModeChanged;
  $('bookSelect').onchange=()=>{ $('lessonSearch').value=''; fillChapters(); };
  $('chapterSelect').onchange=fillLessons;
  $('unitSelect').onchange=selectLesson;
  $('lessonSearch').oninput=()=>fillChapters();
  $('readLesson').onclick=()=>{if(!lessonDetail)return;$('sourceTitle').textContent=lessonDetail.title;$('sourceText').textContent=lessonDetail.text;$('sourceDialog').showModal();};
  $('readStudyPlan').onclick=()=>showSource('study-schedule');
  $('learnedToggle').onchange=async()=>{if(!lessonDetail)return;try{lessonDetail=await api('/api/library/'+lessonDetail.id+'/learned',{learned:$('learnedToggle').checked});renderLesson();}catch(err){notice(err.message,true);}};
  fillChapters(saved);studyModeChanged();
}
function matchingUnits(){const term=$('lessonSearch').value.trim().toLowerCase();return libraryData.units.filter(u=>u.book===$('bookSelect').value&&(!term||(u.title+' '+u.chapter).toLowerCase().includes(term)));}
function fillChapters(saved={}){const planned=$('bookSelect').value==='plan';const chapters=planned?(libraryData.weeks||[]).filter(w=>matchingUnits().some(u=>u.week_ids?.includes(w.id))).map(w=>({id:w.id,title:w.title})):[...new Set(matchingUnits().map(u=>u.chapter))].map(c=>({id:c,title:c}));const old=saved.chapter||$('chapterSelect').value;$('chapterSelectLabel').textContent=planned?'选择周次':'章节／文章';$('unitSelectLabel').textContent=planned?'本次练习的完整文章':'本次练习的小节';$('chapterSelect').innerHTML=chapters.map(c=>`<option value="${e(c.id)}">${e(c.title)}</option>`).join('');if(chapters.some(c=>c.id===old))$('chapterSelect').value=old;fillLessons(saved.unit);renderWorkspaceHome();}
function selectedWeekUnits(){const planned=$('bookSelect').value==='plan';const units=matchingUnits().filter(u=>planned?u.week_ids?.includes($('chapterSelect').value):u.chapter===$('chapterSelect').value);const order=libraryData.weeks?.find(w=>w.id===$('chapterSelect').value)?.articles||[];return planned?units.filter(u=>currentStudyDay()==='all'||u.schedule_days?.includes(Number(currentStudyDay()))).sort((a,b)=>order.indexOf(a.id)-order.indexOf(b.id)):units;}
function fillLessons(preferred){ensureStudyDay(typeof preferred==='string'?preferred:undefined);const units=selectedWeekUnits();const old=typeof preferred==='string'?preferred:$('unitSelect').value;$('unitSelect').innerHTML=units.map(u=>`<option value="${e(u.id)}">${e(u.title)}${u.complete?' ✓':u.covered?' · 已练习':u.learned?' · 已学习':''}</option>`).join('');if(units.some(u=>u.id===old))$('unitSelect').value=old;selectLesson();renderWorkspaceHome();}
async function selectLesson(){const id=$('unitSelect').value;const request=++lessonRequest;lessonDetail=null;if($('practiceType').value==='study')$('startSession').disabled=true;$('lessonPreview').textContent=id?'正在读取本机进度…':'没有匹配的文章，请换个关键词。';$('readLesson').disabled=!id;$('learnedToggle').disabled=!id;renderWorkspaceHome();if(!id)return;try{const d=await api('/api/library/'+id);if(request!==lessonRequest)return;lessonDetail=d;$('startSession').disabled=false;localStorage.setItem('study-selection',JSON.stringify({book:d.book,chapter:$('chapterSelect').value,unit:d.id}));renderLesson();}catch(err){notice(err.message,true);}}
function studyUsage(u){if(!u)return '';const t=u.totals;const n=v=>v===null?'未返回':Number(v).toLocaleString();return `本节累计 Token：输入 ${n(t.input)} · 输出 ${n(t.output)} · 合计 ${n(t.total)}${u.missing.total?'（部分请求未返回用量）':''}`;}
function renderLesson(){const d=lessonDetail;if(!d)return;const c=d.stats;const entry=libraryData.units.find(u=>u.id===d.id);if(entry)Object.assign(entry,c);$('learnedToggle').checked=c.learned;$('lessonPreview').innerHTML=`<p class="lesson-stats">${c.total?`考查覆盖 ${c.covered}/${c.total} · 已通过 ${c.passed}/${c.total}`:'考点清单尚未生成'}${c.complete?' · 本节练习完成':''}</p><p class="hint">${studyUsage(d.usage)}</p><details><summary>本节考点与通过标准</summary>${coverageHtml(d.plan,d.progress)}</details><p class="hint">三题后由你选择继续或复盘。复盘不会清空考点进度。较长小节按原文顺序分段，所有分段通过才算完成。</p>`;
  const siblings=d.full_article?libraryData.units.filter(u=>u.full_article&&u.week_ids?.includes($('chapterSelect').value)):libraryData.units.filter(u=>u.book===d.book&&u.chapter===d.chapter);const passed=siblings.filter(u=>u.id===d.id?c.complete:u.complete).length;
  $('chapterProgress').textContent=d.full_article?`本周 ${passed}/${siblings.length} 篇文章已完成。本篇作为一个连续练习，覆盖全文；退出后可从本机进度继续。`:`本章／文章：${passed}/${siblings.length} 个小节或分段已完成。只有全部通过才标记本章完成。`;
  $('weekInfo').hidden=!d.full_article;
  $('readLesson').textContent=d.full_article?'阅读完整文章':'阅读本节原文';
  $('learnedLabel').textContent=d.full_article?'我已学习这篇文章':'我已学习本节';
  if(d.full_article){
    const week=libraryData.weeks.find(w=>w.id===$('chapterSelect').value);
    const days=(week?.days||[]).filter(x=>d.schedule_days.includes(x.day)&&(currentStudyDay()==='all'||x.day===Number(currentStudyDay())));
    $('weekTasks').innerHTML=days.map(x=>`<p><strong>第 ${x.day} 天 · 配套实战</strong><br>${e(x.practice)}</p><p><strong>完成标准</strong><br>${e(x.goal)}</p>`).join('');
    $('lessonPreview').innerHTML=`<p class="lesson-stats">整篇 ${d.text.length.toLocaleString()} 字符 · ${c.total?`已考查 ${c.covered}/${c.total} · 已通过 ${c.passed}/${c.total}`:'首次练习会依据全文建立考点清单'}</p><p class="hint">重点练理解原理、选择方案、排查问题、项目应用。全文作为练习范围，后续每题只发送相关原文。</p><p class="hint">${studyUsage(d.usage)}</p><details><summary>整篇考点与通过进度</summary>${coverageHtml(d.plan,d.progress)}</details><p class="hint">先练三题，再由你选择继续、复盘或暂停；三题不代表全文练完。</p>`;
  }
  renderWorkspaceHome();
}
function studyPayload(){if($('practiceType').value!=='study')return {};if(!lessonDetail)throw Error('请先选择教材文章。');return {mode:'study',unit_id:lessonDetail.id};}
function renderStudySession(){const s=state.session;const panel=$('studyProgress');panel.hidden=s?.mode!=='study';if(panel.hidden)return;const c=s.study_counts||{total:0,covered:0,passed:0};const entry=libraryData?.units.find(u=>u.id===s.study_unit.id);if(entry)Object.assign(entry,c);const ps=s.study_progress||{points:{}};
  panel.innerHTML=`<div class="study-progress-heading"><div><span class="eyebrow">${e(libraryData?.books.find(b=>b.id===s.study_unit.book)?.title||'教材练习')}</span><h2>${e(s.study_unit.title)}</h2><p class="hint">${e(s.study_unit.full_article?"整篇连续练习 · "+s.study_unit.original_group:s.study_unit.chapter)}</p></div><strong>${c.complete?'本节练习完成':`${c.passed} / ${c.total} 考点通过`}</strong></div><div class="coverage-bars"><label>已考查 ${c.covered}/${c.total}<progress max="${c.total||1}" value="${c.covered}"></progress></label><label>已通过 ${c.passed}/${c.total}<progress max="${c.total||1}" value="${c.passed}"></progress></label></div><details><summary>查看考点清单、通过标准与反馈</summary>${coverageHtml(s.study_plan,ps)}</details><p class="hint">${studyUsage(s.study_usage)}</p><p class="hint">已回答 ${s.turns.filter(t=>t.result).length} 题 · 原回答、考点判定和进度均保存在本机。清单由 AI 依据本节提炼，通过代表本次练习判定。</p>`;
  if(s.awaiting_continue&&s.status!=='completed'&&!s.busy){const gate=document.createElement('section');gate.className='study-checkpoint';gate.innerHTML=`<h2>${c.complete?'本节清单已全部通过':'这一段练习完成了'}</h2><p>${c.complete?'可以主动生成复盘，或选择下一小节。':`已通过 ${c.passed}/${c.total} 个考点，还有 ${c.total-c.passed} 个待练或待巩固。接下来由你决定。`}</p><div class="study-checkpoint-actions">${s.current?'<button id="continueStudy" class="primary">继续下一题</button>':'<button id="nextStudy" class="primary">选择下一小节</button>'}<button id="reviewStudy" class="quiet">开始复盘</button><button id="pauseStudy" class="quiet">先暂停，保留进度</button></div><p class="hint">继续显示随本轮反馈准备的问题，不额外调用 AI；复盘会调用一次 AI。</p>`;$('conversation').append(gate);
    $('continueStudy')?.addEventListener('click',async()=>{const b=$('continueStudy');b.disabled=true;try{await api('/api/sessions/'+s.id+'/continue',{});await loadSession(s.id);}catch(err){notice(err.message,true);b.disabled=false;}});
    $('reviewStudy').onclick=()=>$('endSession').click();$('pauseStudy').onclick=newSession;$('nextStudy')?.addEventListener('click',newSession);
  }
}
