from pydantic import BaseModel
from decimal import Decimal


class ProductBase(BaseModel):
    productname: str
    productprice: Decimal
    description: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    productname: str | None = None
    productprice: Decimal | None = None
    description: str | None = None


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True
