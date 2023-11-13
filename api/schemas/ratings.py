from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .orders import OrderBase



class RatingBase(BaseModel):
    customer_name: str(50) = None
    rating: int
    description: Optional[str] = None
    


class RatingCreate(RatingBase):
    pass


class RatingUpdate(BaseModel):
    customer_name: Optional[str] = None
    rating: int
    description: Optional[str] = None
    



class Rating(RatingBase):
    id: int
    rating_date: Optional[datetime] = None
    order: Optional[OrderBase] = None

    class ConfigDict:
        from_attributes = True
