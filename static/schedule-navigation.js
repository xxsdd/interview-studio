'use strict';
// A day is a view of existing article IDs, never a new practice/progress record.
const StudySchedule = {
  weekArticles(catalog,weekId){
    const week=catalog.weeks.find(w=>w.id===weekId);
    const byId=new Map(catalog.units.filter(u=>u.full_article).map(u=>[u.id,u]));
    return (week?.articles||[]).map(id=>byId.get(id)).filter(Boolean);
  },
  dayArticles(catalog,weekId,day='all'){
    return this.weekArticles(catalog,weekId).filter(u=>day==='all'||u.schedule_days?.includes(Number(day)));
  },
  dayForArticle(catalog,weekId,articleId){
    const week=catalog.weeks.find(w=>w.id===weekId);
    const article=this.weekArticles(catalog,weekId).find(u=>u.id===articleId);
    return week?.days.find(d=>article?.schedule_days?.includes(d.day))?.day;
  }
};
if(typeof module!=='undefined')module.exports=StudySchedule;
