from src.services import assignments,datasets,plans,traces
from src.services.audit import log
def save_dataset(data,user,item_id=None):
 row=datasets.save(data,item_id);log(user.email,'dataset.save',row['name']);return row
def save_plan(data,user,item_id=None):
 row=plans.save(data,item_id);log(user.email,'plan.save',row['name']);return row
def start_trace(data,user):
 row=traces.create(data,user);log(user.email,'trace.queue',row['name']);return row
def grant_sensor(data,user):
 row=assignments.create(data);log(user.email,'assignment.grant',f"dataset={row['dataset_id']} user={row['user_id']} sensor={row['sensor_id']}");return row
def revoke_sensor(item_id,user):
 r=assignments.revoke(item_id);log(user.email,'assignment.revoke',f"assignment={item_id} invalidated={r['invalidated']}");return r
