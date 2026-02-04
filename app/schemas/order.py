from pydantic import BaseModel
from datetime import datetime
from app.models.enums import OrderStatus


class OrderCreate(BaseModel):
    order_item: str


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderRead(BaseModel):
    id: int
    order_number: str
    order_item: str
    status: OrderStatus
    order_date: datetime

    class Config:
        from_attributes = True
