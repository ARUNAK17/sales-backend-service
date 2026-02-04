from sqlalchemy import Column, String, Integer, Numeric, DateTime
from app.db.base import Base
from datetime import datetime

class SalesRecord(Base):
    __tablename__ = "sales_records"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    sale_amount = Column(Numeric, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow, nullable=False)
