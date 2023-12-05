from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Promo(Base):
    __tablename__ = "promos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promo_code = Column(String(20), unique=True, nullable=True)
    discount = Column(DECIMAL(4, 2), nullable=False, server_default='0.0')
    expiration_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))


