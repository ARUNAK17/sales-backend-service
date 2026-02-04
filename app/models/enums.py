from enum import Enum

class Userrole(str,Enum):
    CEO = "CEO"
    Salesperson = "Salesperson"
    Customer = "Customer"

class OrderStatus(str, Enum):
    CREATED = "CREATED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
