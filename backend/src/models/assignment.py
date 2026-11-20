from sqlalchemy import Column,Integer,DateTime,func,ForeignKey,UniqueConstraint
from src.config.database import Base
class Assignment(Base):
 __tablename__='assignments'
 id=Column(Integer,primary_key=True)
 dataset_id=Column(Integer,ForeignKey('datasets.id'),nullable=False)
 user_id=Column(Integer,ForeignKey('users.id'),nullable=False)
 sensor_id=Column(Integer,nullable=False)
 created_at=Column(DateTime,server_default=func.now())
 __table_args__=(UniqueConstraint('dataset_id','user_id','sensor_id',name='uq_assignment'),)
