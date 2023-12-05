from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import order_details as odModel
from ..models import sandwiches as sandModel
from ..models import promos as promoModel
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description,
        card_number=request.card_number,
        cvv=request.cvv,
        card_name=request.card_name,
        exp_month=request.exp_month,
        exp_year=request.exp_year,
        sandwich_id=request.sandwich_id,
        amount=request.amount,
        promo_code=request.promo_code
        )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
            
    item = db.query(model.Order).filter().first()
    promo = db.query(promoModel.Promo).filter(promoModel.Promo.promo_code == request.promo_code).first()

    discount = 0

    if promo != None:
        discount = promo.discount

    new_order_detail = odModel.OrderDetail(
        order_id=item.id,
        sandwich_id=new_item.sandwich_id,
        amount=new_item.amount,
        total_price = new_item.amount * (db.query(sandModel.Sandwich).filter(sandModel.Sandwich.id == new_item.sandwich_id).first().price) - discount
        # Add other fields here
    )
    db.add(new_item)
    db.add(new_order_detail)
    db.commit()
    db.refresh(new_item)
    db.refresh(new_order_detail)

    numSandwiches = db.query(sandModel.Sandwich).filter(sandModel.Sandwich.id == new_item.sandwich_id).first().amount
    
    if (numSandwiches - new_order_detail.amount) < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough sandwiches")
    
    sandwich = db.query(sandModel.Sandwich).filter(sandModel.Sandwich.id == new_item.sandwich_id).first()
    sandwich.amount -= new_order_detail.amount
    db.commit()
    try:
        print(new_order_detail)
        db.add(new_order_detail)
        db.commit()
        db.refresh(new_order_detail)
        
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
            

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_date(db: Session, date):
    try:
        result = db.query(model.Order).filter(func.date(model.Order.order_date) == date)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders on that date!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def get_total_cost(db: Session, date):
    total_cost = db.query(func.sum(odModel.OrderDetail.total_price)).\
        join(model.Order, model.Order.id == odModel.OrderDetail.order_id).\
        filter(func.date(model.Order.order_date)).\
        scalar()
    print(total_cost)
    return {"total_cost": total_cost or 0.0}


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
