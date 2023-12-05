from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import ratings as model
from ..models import orders as orderModel
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.Rating(
        rating=request.rating,
        description=request.description,
        customer_name=request.customer_name,
        order_id=request.order_id
    )
    order_object = db.query(orderModel.Order).filter(orderModel.Order.id == new_item.order_id).first()
    if not order_object:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Id not found!")
    

    #setting rating values lower than 1 and higher than 10 to 1 or 10 respectivley to keep ratings within 1-10 range
    if new_item.rating < 1:
        new_item.rating = 1
    if new_item.rating > 10:
        new_item.rating = 10

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

def read_all(db: Session):
    try:
        result = db.query(model.Rating).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Rating).filter(model.Rating.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Rating).filter(model.Rating.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        #setting rating values lower than 1 and higher than 10 to 1 or 10 respectivley to keep ratings within 1-10 range when updated
        if request.rating < 1:
            update_data['rating'] = 1
        if request.rating > 10:
            update_data['rating'] = 10
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Rating).filter(model.Rating.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



