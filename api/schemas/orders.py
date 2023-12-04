from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail



class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None
    order_complete: bool = False
    card_number: str = "0123 4567 8910 1112"
    cvv: str = "000"
    card_name: str
    exp_month: str = "00"
    exp_year: str = "00"


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    order_complete: Optional[bool] = None
    card_number: str
    cvv: str = None
    card_name: str
    exp_month: str = "00"
    exp_year: str = "00"



class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
