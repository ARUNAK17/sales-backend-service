from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum
from app.db.base import Base
from datetime import datetime
from app.models.enums import OrderStatus

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, nullable=False)
    order_item = Column(String, nullable=False)
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.CREATED)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
