
from .. import models, schemas, utils
from fastapi import  Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.post("/user",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users",status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users= db.query(models.User).all()
    return {"data": users}

@router.get("/user/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} was not found")
    return user