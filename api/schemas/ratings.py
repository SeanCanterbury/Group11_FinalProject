from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .orders import OrderBase



class RatingBase(BaseModel):
    customer_name: str
    rating: int
    description: Optional[str] = None
    order_id: int
    


class RatingCreate(RatingBase):
    pass
    



class RatingUpdate(BaseModel):
    customer_name: Optional[str] = None
    rating: int
    description: Optional[str] = None
    



class Rating(RatingBase):
    id: int
    rating_date: Optional[datetime] = None
    order_id: int

    class ConfigDict:
        from_attributes = True
