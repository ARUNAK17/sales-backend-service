from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime, date


class SalesRecordRead(BaseModel):
    id: int
    order_number: str
    product_name: str
    sale_amount: Decimal
    sale_date: datetime

    class Config:
        from_attributes = True


class ProductSalesStats(BaseModel):
    product_name: str
    total_sales: Decimal


class ProductRankStats(BaseModel):
    product_name: str
    quarter: int
    total_sales: Decimal
    rank: int


class CumulativeSalesStats(BaseModel):
    sale_date: date
    daily_sales: Decimal
    cumulative_sales: Decimal
