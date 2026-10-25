'use strict';
// Navigation and presentation only: viewing the library never requests generation.
const workspace = {shelf:'plan', filter:'all', libraryDay:'all', request:0, history:[]};
let studyDays={};try{studyDays=JSON.parse(localStorage.getItem('study-days')||'{}');}catch{}
function currentStudyDay(){return studyDays[$('chapterSelect').value]??'all';}
function ensureStudyDay(preferred){
  if(!libraryData||$('bookSelect').value!=='plan')return;
  const weekId=$('chapterSelect').value,week=libraryData.weeks.find(w=>w.id===weekId);if(!week)return;
  let day=studyDays[weekId];
  if(preferred){const article=StudySchedule.weekArticles(libraryData,weekId).find(u=>u.id===preferred);if(article&&!(day==='all'||article.schedule_days.includes(Number(day))))day=StudySchedule.dayForArticle(libraryData,weekId,preferred);}
  if(day!=='all'&&!week.days.some(d=>d.day===Number(day)))day=StudySchedule.dayForArticle(libraryData,weekId,$('unitSelect').value)||week.days[0]?.day;
  const matching=matchingUnits().filter(u=>u.week_ids?.includes(weekId));
  if($('lessonSearch').value.trim()&&day!=='all'&&matching.length&&!matching.some(u=>u.schedule_days.includes(Number(day))))day=StudySchedule.dayForArticle(libraryData,weekId,matching[0].id);
  studyDays[weekId]=day;localStorage.setItem('study-days',JSON.stringify(studyDays));
}
function renderStudyDays(){
  const planned=$('bookSelect').value==='plan';$('dayNavigation').hidden=!planned;if(!planned)return;
  const weekId=$('chapterSelect').value,week=libraryData.weeks.find(w=>w.id===weekId),day=currentStudyDay();
  if(!week){$('dayTabs').innerHTML='';$('dayProgress').textContent='';$('dayTask').hidden=true;return;}
  const tabs=[...week.days.map(d=>({id:String(d.day),title:`第 ${d.day} 天`,articles:StudySchedule.dayArticles(libraryData,weekId,d.day)})),{id:'all',title:'整周',articles:StudySchedule.weekArticles(libraryData,weekId)}];
  const key=weekId+'|'+day+'|'+tabs.map(t=>t.articles.map(u=>`${u.id}:${u.learned}:${u.complete}`).join(',')).join(';');
  if(workspace.dayKey!==key){workspace.dayKey=key;$('dayTabs').innerHTML=tabs.map(t=>`<button type="button" role="tab" id="study-day-${t.id}" aria-controls="articleRows" aria-selected="${t.id===String(day)}" tabindex="${t.id===String(day)?0:-1}" data-day="${t.id}">${t.title}<small>${t.articles.length} 篇</small></button>`).join('');}
  $('dayTabs').querySelectorAll('[data-day]').forEach(b=>b.onclick=()=>{const chosen=b.dataset.day;studyDays[weekId]=chosen;localStorage.setItem('study-days',JSON.stringify(studyDays));$('lessonSearch').value='';fillLessons();$('dayTabs').querySelector(`[data-day="${chosen}"]`)?.focus();});bindTabKeys($('dayTabs'));
  const articles=StudySchedule.dayArticles(libraryData,weekId,day);$('dayProgress').textContent=`${day==='all'?'本周':'第 '+day+' 天'}：已学习 ${articles.filter(u=>u.learned).length}/${articles.length} 篇 · 练习通过 ${articles.filter(u=>u.complete).length}/${articles.length} 篇。重复安排的文章共用进度。`;
  const task=week.days.find(d=>d.day===Number(day));$('dayTask').hidden=!task;
  if(task){$('dayTaskTitle').textContent=`第 ${day} 天的实战与完成标准`;$('dayTaskContent').innerHTML=`<p><strong>配套实战</strong><br>${e(task.practice)}</p><p><strong>完成标准</strong><br>${e(task.goal)}</p>`;}
  $('dayNavigation').setAttribute('role','tabpanel');$('dayNavigation').setAttribute('aria-labelledby',$('weekTabs').querySelector('[aria-selected=true]')?.id||'articleListTitle');
}
function articleStatus(u){return u.complete?'已通过':u.covered?'练习中':u.learned?'已学习':'未学习';}
function progressText(u){return u.total?`考查 ${u.covered}/${u.total} · 通过 ${u.passed}/${u.total}`:'尚未生成考点';}
function workspaceView(){window.refreshModelChoice?.();document.body.dataset.view=state.session?'practice':'home';$('sessionTitle').textContent=document.body.classList.contains('history-view')?'练习记录':state.session?.title||'学习计划';$('focusAnswer').hidden=$('composer').hidden;$('mobileNav').setAttribute('aria-expanded','false');document.body.classList.remove('nav-open');syncNavigation();}
function syncNavigation(){const narrow=matchMedia('(max-width:800px)').matches;const open=narrow&&document.body.classList.contains('nav-open');$('workspaceSidebar').inert=narrow&&!open;document.querySelector('main').inert=open;}
function renderWorkspaceHome(){
  if(!libraryData)return;
  workspaceView();
  const planned=$('bookSelect').value==='plan';
  $('weekTabs').hidden=!planned;
  const weekKey=$('bookSelect').value+'|'+$('chapterSelect').value;
  if(workspace.weekKey!==weekKey){workspace.weekKey=weekKey;$('weekTabs').innerHTML=(libraryData.weeks||[]).map((w,i)=>`<button type="button" role="tab" id="weekTab${i}" aria-controls="dayNavigation" aria-selected="${w.id===$('chapterSelect').value}" tabindex="${w.id===$('chapterSelect').value?0:-1}" data-week="${e(w.id)}">第${['一','二','三'][i]}周<small>${e(w.title.replace(/^第.周[：:]\s*/,''))}</small></button>`).join('');}
  renderStudyDays();
  $('articleRows').setAttribute('role',planned?'tabpanel':'group');if(planned)$('articleRows').setAttribute('aria-labelledby',$('dayTabs').querySelector('[aria-selected=true]')?.id||'articleListTitle');else $('articleRows').setAttribute('aria-labelledby','articleListTitle');
  $('weekTabs').querySelectorAll('[data-week]').forEach(b=>b.onclick=()=>{const week=b.dataset.week;$('chapterSelect').value=week;fillLessons();$('weekTabs').querySelector(`[data-week="${week}"]`)?.focus();});
  bindTabKeys($('weekTabs'));
  const units=selectedWeekUnits();
  $('articleListTitle').textContent=planned?(currentStudyDay()==='all'?'本周完整文章':`第 ${currentStudyDay()} 天 · 完整文章`):$('chapterSelect').value||'教材小节';
  $('articleListCount').textContent=`${units.length} ${planned?'篇':'节'} · ${units.filter(u=>u.complete).length} 已通过`;
  $('articleRows').innerHTML=units.map((u,i)=>`<button class="article-row ${u.id===$('unitSelect').value?'selected':''}" data-unit="${e(u.id)}" aria-pressed="${u.id===$('unitSelect').value}"><span class="article-index">${String(i+1).padStart(2,'0')}</span><span class="article-copy"><strong>${e(u.title)}</strong><small>${e(progressText(u))}</small></span><span class="status-chip ${u.complete?'passed':''}">${articleStatus(u)}</span></button>`).join('')||'<p class="empty-state">没有找到文章，试试更短的关键词。</p>';
  $('articleRows').querySelectorAll('[data-unit]').forEach(b=>b.onclick=async()=>{$('unitSelect').value=b.dataset.unit;await selectLesson();if(matchMedia('(max-width:1150px)').matches)document.querySelector('.selection-panel').scrollIntoView({block:'start',behavior:'smooth'});});
  $('selectedArticleTitle').textContent=lessonDetail?.title||'选择一篇文章';
  $('selectionTools').hidden=!planned;
  $('articleBrowser').hidden=$('practiceType').value!=='study';
  const last=workspace.history.find(s=>s.id===localStorage.getItem('workspace-last-session')&&s.status!=='completed')||workspace.history.find(s=>s.status!=='completed');
  $('resumePractice').hidden=!last;
  if(last){$('resumeTitle').textContent=last.title;$('resumeMeta').textContent=`${last.turns} 次回答 · 本机已保存`;$('resumeButton').onclick=()=>loadSession(last.id).then(()=>{document.querySelector('.conversation>.message:last-of-type')?.scrollIntoView({block:'start'});}).catch(err=>notice(err.message,true));}
}
function bindTabKeys(container){container.onkeydown=ev=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(ev.key))return;const tabs=[...container.querySelectorAll('[role=tab]')];if(!tabs.length)return;let i=tabs.indexOf(document.activeElement);if(i<0)i=0;i=ev.key==='Home'?0:ev.key==='End'?tabs.length-1:(i+(ev.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;ev.preventDefault();tabs[i].focus();tabs[i].click();};}
function openLibrary(){workspace.request++;$('bankDialog').showModal();renderLibraryBrowser();}
function renderLibraryBrowser(){
  if(!libraryData||!state.catalog)return;
  const shelf=workspace.shelf;
  $('libraryResults').setAttribute('aria-labelledby','shelf-'+shelf);
  $('libraryTabs').querySelectorAll('[data-shelf]').forEach(b=>{const active=b.dataset.shelf===shelf;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;});
  const filter=$('libraryFilter');const before=workspace.filter;
  const options=shelf==='plan'?(libraryData.weeks||[]).map(w=>({id:w.id,title:w.title})):shelf==='textbooks'?libraryData.books.filter(b=>b.id!=='plan'):Object.keys(state.catalog.topics).map(t=>({id:t,title:t}));
  filter.innerHTML='<option value="all">全部'+(shelf==='plan'?'周次':shelf==='textbooks'?'分类':'主题')+'</option>'+options.map(o=>`<option value="${e(o.id)}">${e(o.title)}</option>`).join('');filter.value=options.some(o=>o.id===before)?before:'all';workspace.filter=filter.value;
  $('libraryDayControl').hidden=shelf!=='plan';
  const days=(libraryData.weeks||[]).filter(w=>filter.value==='all'||w.id===filter.value).flatMap(w=>w.days);
  if(!days.some(d=>String(d.day)===workspace.libraryDay))workspace.libraryDay='all';
  $('libraryDay').innerHTML='<option value="all">全部天数</option>'+days.map(d=>`<option value="${d.day}">第 ${d.day} 天</option>`).join('');$('libraryDay').value=workspace.libraryDay;
  $('libraryFilterLabel').textContent=shelf==='plan'?'按周次查看':shelf==='textbooks'?'按教材分类':'按面试主题';
  const query=$('bankSearch').value.trim().toLowerCase();
  const matches=(...texts)=>texts.join(' ').toLowerCase().includes(query);
  let entries=[];
  if(shelf==='plan'){
    entries=libraryData.units.filter(u=>u.full_article&&(filter.value==='all'||u.week_ids.includes(filter.value))&&(workspace.libraryDay==='all'||u.schedule_days.includes(Number(workspace.libraryDay)))&&matches(u.title,u.original_group));
    $('bankStats').textContent=`${libraryData.units.filter(u=>u.full_article).length} 篇完整文章 · 依三周计划练习 · 进度跨周共享`;
    $('bankList').innerHTML=entries.map(u=>`<button class="bank-item library-article" data-library-unit="${e(u.id)}"><span><strong>${e(u.title)}</strong><small>${e(u.original_group)} · 第 ${u.schedule_days.join('、')} 天<br>${e(progressText(u))}</small></span><span class="status-chip ${u.complete?'passed':''}">${articleStatus(u)}</span></button>`).join('');
  }else if(shelf==='textbooks'){
    const groups=new Map();for(const u of libraryData.units.filter(u=>!u.full_article)){if(!groups.has(u.source))groups.set(u.source,{...u,sections:[]});groups.get(u.source).sections.push(u);}
    entries=[...groups.values()].filter(u=>(filter.value==='all'||u.book===filter.value)&&matches(u.chapter,...u.sections.map(s=>s.title)));
    $('bankStats').textContent=`${libraryData.documents} 份原有教材 · 按原文归档 · 保留历史小节进度`;
    $('bankList').innerHTML=entries.map(u=>`<button class="bank-item" data-library-source="${e(u.source)}"><strong>${e(u.chapter)}</strong><small>${e(libraryData.books.find(b=>b.id===u.book)?.title)} · ${u.sections.length} 个原有练习单元 · ${u.sections.filter(s=>s.complete).length} 已通过</small></button>`).join('');
  }else{
    entries=state.catalog.questions.filter(q=>(filter.value==='all'||q.topic===filter.value)&&matches(q.title,q.topic));
    $('bankStats').textContent=`${state.catalog.count} 道现成面试题 · ${Object.keys(state.catalog.topics).length} 个主题 · 与教材考点分别计数`;
    $('bankList').innerHTML=entries.map(q=>`<button class="bank-item" data-question="${e(q.id)}"><strong>${e(q.title)}</strong><small>${e(q.id)} · ${e(q.topic)} · ${e(q.difficulty)} · ${e(q.importance)}</small></button>`).join('');
  }
  $('libraryResultCount').textContent=`找到 ${entries.length} ${shelf==='questions'?'道题':'篇资料'}`;
  if(!entries.length)$('bankList').innerHTML='<p class="empty-state">没有找到匹配内容，请换个分类或关键词。</p>';
  $('libraryDetail').hidden=true;$('bankList').hidden=false;
  $('bankList').querySelectorAll('[data-library-unit]').forEach(b=>b.onclick=()=>previewLibraryUnit(b.dataset.libraryUnit));
  $('bankList').querySelectorAll('[data-library-source]').forEach(b=>b.onclick=()=>previewTextbook(b.dataset.librarySource));
  $('bankList').querySelectorAll('[data-question]').forEach(b=>b.onclick=async()=>{try{const q=await api('/api/question/'+b.dataset.question);$('sourceTitle').textContent=q.title;$('sourceText').textContent=q.text;$('sourceDialog').showModal();}catch(err){notice(err.message,true);}});
}
async function previewLibraryUnit(id){
  const request=++workspace.request;const panel=$('libraryDetail');panel.hidden=false;$('bankList').hidden=true;panel.innerHTML='<p role="status">正在读取本机考点…</p>';
  try{const d=await api('/api/library/'+id);if(request!==workspace.request)return;panel.innerHTML=`<button id="libraryBack" class="quiet">返回资料列表</button><h3>${e(d.title)}</h3><p class="lesson-stats">${e(progressText(d.stats))}</p><div class="library-detail-actions"><button class="primary" id="chooseLibraryArticle">选择这篇文章</button><button class="quiet" id="readLibraryArticle">阅读完整原文</button></div><p class="hint">${d.plan?'以下考点已保存在本机。':'这篇文章还没有考点清单。开始练习时才会依据全文生成，浏览不调用 AI。'}</p>${d.plan?coverageHtml(d.plan,d.progress):''}`;
    $('libraryBack').onclick=()=>{workspace.request++;panel.hidden=true;$('bankList').hidden=false;$('bankList').querySelector(`[data-library-unit="${id}"]`)?.focus();};$('chooseLibraryArticle').onclick=()=>chooseLibraryUnit(id);$('readLibraryArticle').onclick=()=>{$('sourceTitle').textContent=d.title;$('sourceText').textContent=d.text;$('sourceDialog').showModal();};panel.scrollTop=0;panel.focus();
  }catch(err){if(request===workspace.request)panel.textContent=err.message;}
}
function previewTextbook(source){
  workspace.request++;const units=libraryData.units.filter(u=>!u.full_article&&u.source===source);const panel=$('libraryDetail');panel.hidden=false;$('bankList').hidden=true;panel.innerHTML=`<button id="libraryBack" class="quiet">返回资料列表</button><h3>${e(units[0].chapter)}</h3><button class="quiet" id="readLibrarySource">阅读完整原文</button><p class="hint">以下是已有的小节练习；三周计划中的文章采用整篇连续练习。</p>${units.map(u=>`<button class="bank-item" data-legacy-unit="${e(u.id)}"><strong>${e(u.title)}</strong><small>${articleStatus(u)} · ${e(progressText(u))}</small></button>`).join('')}`;$('libraryBack').onclick=()=>{panel.hidden=true;$('bankList').hidden=false;$('bankList').querySelector('[data-library-source="'+source+'"]')?.focus();};$('readLibrarySource').onclick=()=>showSource(source);panel.querySelectorAll('[data-legacy-unit]').forEach(b=>b.onclick=()=>chooseLibraryUnit(b.dataset.legacyUnit));panel.focus();
}
async function chooseLibraryUnit(id){
  const u=libraryData.units.find(x=>x.id===id);if(!u)return;
  await newSession();if(state.session)return;
  const week=u.full_article?(libraryData.weeks.find(w=>u.week_ids.includes(w.id)&&(workspace.libraryDay!=='all'?w.days.some(d=>String(d.day)===workspace.libraryDay):w.id===workspace.filter))?.id||u.week_ids[0]):null;
  if(week&&workspace.libraryDay!=='all')studyDays[week]=workspace.libraryDay;
  $('practiceType').value='study';studyModeChanged();$('bookSelect').value=u.book;$('lessonSearch').value='';fillChapters({chapter:week||u.chapter,unit:id});$('bankDialog').close();$('selectedArticleTitle').scrollIntoView({block:'center'});
}
function initWorkspace(){
  document.body.classList.add('workspace-v2');
  document.querySelector('.selection-panel').before($('bankSetup'));
  document.querySelector('.selection-panel').append($('lessonPreview'),$('weekInfo'));
  // Keep IDs and form behavior shared with the existing recording and study flow.
  const prefs=document.createElement('details');prefs.className='practice-preferences';prefs.innerHTML='<summary>练习语言与偏好</summary>';
  const firstLabel=document.querySelector('.sidebar>label');firstLabel.before(prefs);for(const id of ['language','feedbackLanguage','inputLanguage']){prefs.append(document.querySelector(`label[for="${id}"]`),$(id));}prefs.append(document.querySelector('.side-note'));document.querySelector('.sidebar>.side-label').remove();
  $('bankOpen').innerHTML='▤ 学习资料与题库 <span id="bankCount">3 类</span>';
  $('bankOpen').onclick=openLibrary;$('bankSearch').oninput=()=>{workspace.request++;renderLibraryBrowser();};$('libraryFilter').onchange=()=>{workspace.filter=$('libraryFilter').value;workspace.request++;renderLibraryBrowser();};$('libraryDay').onchange=()=>{workspace.libraryDay=$('libraryDay').value;workspace.request++;renderLibraryBrowser();};
  $('libraryTabs').querySelectorAll('[data-shelf]').forEach(b=>b.onclick=()=>{workspace.shelf=b.dataset.shelf;workspace.filter='all';workspace.request++;renderLibraryBrowser();});bindTabKeys($('libraryTabs'));
  $('bankDialog').addEventListener('close',()=>workspace.request++);
  $('mobileNav').onclick=()=>{const open=document.body.classList.toggle('nav-open');$('mobileNav').setAttribute('aria-expanded',String(open));syncNavigation();if(open)$('newSession').focus();};$('navBackdrop').onclick=()=>{document.body.classList.remove('nav-open');$('mobileNav').setAttribute('aria-expanded','false');syncNavigation();$('mobileNav').focus();};
  matchMedia('(max-width:800px)').addEventListener('change',syncNavigation);
  document.addEventListener('keydown',ev=>{if(ev.key==='Escape'&&document.body.classList.contains('nav-open'))$('navBackdrop').click();});
  $('focusAnswer').onclick=()=>{$('composer').scrollIntoView({block:'center',behavior:'smooth'});$('answer').focus({preventScroll:true});};
  workspaceView();
}
initWorkspace();
