from fastapi import APIRouter,Depends
from src.middlewares.auth import admin
from src.schemas.business import AssignmentInput
from src.services import assignments
from src.controllers.business import grant_sensor,revoke_sensor
router=APIRouter()
@router.get('/assignments')
def listing(u=Depends(admin)):return assignments.list_items()
@router.post('/assignments')
def create(data:AssignmentInput,u=Depends(admin)):return grant_sensor(data,u)
@router.delete('/assignments/{item_id}')
def revoke(item_id:int,u=Depends(admin)):return revoke_sensor(item_id,u)
