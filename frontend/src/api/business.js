import {api,post} from './client.js';
export const datasets={list:()=>api('/datasets'),save:(d,id)=>post('/datasets'+(id?'/'+id:''),d,id?'PUT':'POST')};
export const plans={list:()=>api('/plans'),save:(d,id)=>post('/plans'+(id?'/'+id:''),d,id?'PUT':'POST')};
export const traces={list:()=>api('/traces'),run:d=>post('/traces',d),detail:id=>api('/traces/'+id)};
export const assignments={list:()=>api('/assignments'),grant:d=>post('/assignments',d),revoke:id=>api('/assignments/'+id,{method:'DELETE'})};
