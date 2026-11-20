import time,logging,redis
from pathlib import Path
from sqlalchemy import update
from src.config.settings import REDIS_URL
from src.config.database import Session
from src.models.trace import Trace
from src.services.operators import execute
from src.services.audit import log
q=redis.Redis.from_url(REDIS_URL)
def transition(run_id,src,dst,**values):
 with Session() as s:
  res=s.execute(update(Trace).where(Trace.id==run_id,Trace.status==src).values(status=dst,**values));s.commit();return res.rowcount
while True:
 Path('/tmp/worker-heartbeat').touch()
 try:
  item=q.blpop('operator-traces',timeout=2)
  if not item:continue
  run_id=int(item[1])
  with Session() as s:
   row=s.get(Trace,run_id)
   snapshot=row.snapshot if row and row.status=='queued' else None
  if not snapshot or not transition(run_id,'queued','running'):continue
  try:
   result=execute(snapshot['dataset'],snapshot['plan']['steps'])
   if transition(run_id,'running','completed',result=result):log('worker','trace.completed',str(run_id))
   else:log('worker','trace.suppressed',str(run_id))
  except Exception as exc:
   logging.exception('trace failed')
   transition(run_id,'running','failed',error=str(exc)[:1000])
 except Exception:logging.exception('worker loop');time.sleep(2)
