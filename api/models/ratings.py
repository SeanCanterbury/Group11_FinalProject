from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(Integer, nullable=False)
    CheckConstraint('1<=rating AND rating<=10', name='rating_range')
    customer_name = Column(String(100))
    rating_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    order_id = Column(Integer, ForeignKey('orders.id'))
    description = Column(String(300))
    

    #order = relationship("Order", back_populates="order")