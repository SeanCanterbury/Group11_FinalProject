from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import sandwiches as model
from ..models import resources as resModel
from sqlalchemy.exc import SQLAlchemyError



def create(db: Session, request):
    resource = db.query(resModel.Resource).filter(resModel.Resource.id == request.resource_id).first()
    
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    resource.amount -= 1

    if resource.amount < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough resources")

    new_item = model.Sandwich(
        sandwich_name=request.sandwich_name,
        price=request.price,
        calories=request.calories,
        resource_id=request.resource_id

    )

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
        result = db.query(model.Sandwich).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        
        if 'resource_id' in request.dict():
            # Fetch the corresponding resource
            resource = db.query(resModel.Resource).filter(resModel.Resource.id == request.resource_id).first()
            
            # If the resource does not exist, raise a 404 error
            if not resource:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

            # Subtract one from the resource amount
            resource.amount -= 1

            # If the resource amount is less than 0, raise a 400 error
            if resource.amount < 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough resources")

        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
