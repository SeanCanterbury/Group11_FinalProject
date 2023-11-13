from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class PromoBase(BaseModel):
    promo_code: str
    discount: float
    expiration_date: Optional[datetime] = None


class PromoCreate(PromoBase):
    pass


class PromoUpdate(BaseModel):
    promo_code: Optional[str] = None
    discount: float
    expiration_date: Optional[datetime] = None



class Promo(PromoBase):
    id: int
    
    class ConfigDict:
        from_attributes = True
