from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SandwichBase(BaseModel):
    sandwich_name: str
    price: float
    calories: int
    resource_id: int


class SandwichCreate(SandwichBase):
    pass


class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    resource_id: Optional[int] = None


class Sandwich(SandwichBase):
    id: int

    class ConfigDict:
        from_attributes = True