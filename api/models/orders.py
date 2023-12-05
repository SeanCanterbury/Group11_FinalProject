from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"
    #add customer email phone and address, total 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) #acts as tracking number
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    order_complete = Column(Boolean, nullable=False, server_default='0')
    card_number = Column(String(19), nullable=False)
    cvv = Column(String(3), nullable=False)
    card_name = Column(String(300), nullable=False)
    exp_month = Column(String(2), nullable=False)
    exp_year = Column(String(2), nullable=False)
    sandwich_id = Column(Integer, nullable=False)
    amount = Column(Integer, index=True, nullable=False)
    promo_code = Column(String(100))


    order_details = relationship("OrderDetail", back_populates="order")
    #promos = relationship("Promo", back_populates="order")
