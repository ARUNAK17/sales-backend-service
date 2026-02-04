from sqlalchemy import Column,String,Integer,Numeric
from app.db.base import Base

class Product(Base):
    __tablename__="products"
    
    id = Column(Integer,primary_key= True, index= True)
    productname=Column(String,unique=True,index=True)
    productprice = Column(Numeric,nullable=False)
    description = Column(String)