import redis
from fastapi import HTTPException
from sqlalchemy import update
from src.config.database import Session
from src.config.settings import REDIS_URL
from src.models.assignment import Assignment
from src.models.dataset import Dataset
from src.models.identity import User
from src.models.plan import Plan
from src.models.trace import Trace
from src.utils.serialization import record
queue=redis.Redis.from_url(REDIS_URL)
def _emails(s):return {u.id:u.email for u in s.query(User).all()}
def list_items(user):
 with Session() as s:
  q=s.query(Trace)
  if user.role=='operator':q=q.filter(Trace.owner_id==user.id,Trace.status!='invalid')
  elif user.role=='viewer':q=q.filter(Trace.owner_id.isnot(None),Trace.status!='invalid')
  rows=q.order_by(Trace.id.desc()).limit(100).all();emails=_emails(s)
  return [dict(record(r),owner=emails.get(r.owner_id)) for r in rows]
def detail(item_id,user):
 with Session() as s:
  row=s.get(Trace,item_id)
  if not row:raise HTTPException(404,'未找到执行轨迹')
  if user.role!='admin':
   if row.status=='invalid':raise HTTPException(403,'该剖面已因撤权失效，重新授权也不会恢复')
   if row.owner_id is None:raise HTTPException(403,'历史无归属剖面仅管理员查阅')
   if user.role=='operator' and row.owner_id!=user.id:raise HTTPException(403,'只能查看自己的剖面')
  return dict(record(row),owner=_emails(s).get(row.owner_id))
def create(data,user):
 with Session() as s:
  p=s.get(Plan,data.plan_id)
  if not p:raise HTTPException(404,'未找到算子计划')
  d=s.get(Dataset,p.dataset_id)
  ds=record(d)
  if user.role=='operator':
   ids={a.sensor_id for a in s.query(Assignment).filter_by(dataset_id=d.id,user_id=user.id)}
   ds['sensors']=[r for r in ds['sensors'] if r['sensor_id'] in ids]
   ds['readings']=[r for r in ds['readings'] if r['sensor_id'] in ids]
   scope=sorted(ids)
  else:scope=sorted({r['sensor_id'] for r in ds['sensors']}|{r['sensor_id'] for r in ds['readings']})
  row=Trace(name=data.name,plan_id=p.id,dataset_id=d.id,owner_id=user.id,status='queued',snapshot={'dataset':ds,'plan':record(p),'scope':{'sensor_ids':scope,'owner':user.email,'role':user.role}})
  s.add(row);s.commit();s.refresh(row);result=dict(record(row),owner=user.email)
 try:queue.rpush('operator-traces',result['id'])
 except redis.RedisError:
  with Session() as s:s.execute(update(Trace).where(Trace.id==result['id'],Trace.status=='queued').values(status='failed',error='队列不可用，请创建新任务'));s.commit()
  raise HTTPException(503,'队列不可用，请稍后重试')
 return result
