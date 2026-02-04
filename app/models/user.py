from sqlalchemy import Column,String,Integer,Enum as SQLEnum,Boolean
from app.db.base import Base
from app.models.enums import Userrole

class User(Base):
    __tablename__= "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,index=True,nullable=False)
    userrole = Column(SQLEnum(Userrole),nullable=False)
    email = Column(String,unique=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
