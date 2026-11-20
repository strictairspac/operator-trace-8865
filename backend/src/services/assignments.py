from fastapi import HTTPException
from src.config.database import Session
from src.models.assignment import Assignment
from src.models.dataset import Dataset
from src.models.identity import User
from src.models.trace import Trace
from src.utils.serialization import record

def list_items():
 with Session() as s:
  rows=s.query(Assignment).order_by(Assignment.id.desc()).all()
  users={u.id:u.email for u in s.query(User).all()};datasets={d.id:d.name for d in s.query(Dataset).all()}
  return [dict(record(r),user=users.get(r.user_id),dataset=datasets.get(r.dataset_id)) for r in rows]
def create(data):
 with Session() as s:
  u=s.query(User).filter_by(email=data.email).first()
  if not u:raise HTTPException(404,'未找到该助教账号')
  if u.role!='operator':raise HTTPException(400,'只能给助教（operator）分配传感器')
  if not s.get(Dataset,data.dataset_id):raise HTTPException(404,'未找到数据集')
  row=s.query(Assignment).filter_by(dataset_id=data.dataset_id,user_id=u.id,sensor_id=data.sensor_id).first()
  if not row:
   row=Assignment(dataset_id=data.dataset_id,user_id=u.id,sensor_id=data.sensor_id);s.add(row);s.commit();s.refresh(row)
  return record(row)
def revoke(item_id):
 with Session() as s:
  row=s.get(Assignment,item_id)
  if not row:raise HTTPException(404,'未找到授权记录')
  uid,did,sid=row.user_id,row.dataset_id,row.sensor_id
  s.delete(row)
  hits=s.query(Trace).filter(Trace.owner_id==uid,Trace.dataset_id==did,Trace.status!='invalid').all()
  n=0
  for t in hits:
   if sid in ((t.snapshot or {}).get('scope',{}).get('sensor_ids') or []):t.status='invalid';n+=1
  s.commit();return {'revoked':item_id,'invalidated':n}
