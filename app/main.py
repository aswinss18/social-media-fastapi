from fastapi import FastAPI,Response,status,HTTPException,Depends
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext
import time
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session
from . import schemas


app = FastAPI()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)





while True:
    try:
       conn =psycopg2.connect(host='localhost',database='social-media-fastapi',user='postgres',password='4166',cursor_factory=RealDictCursor)
       cursor = conn.cursor()
       print("🟢 🟢 🟢 Database connection was successful! 🟢 🟢 🟢")
       break
    except Exception as error:
       print("🔴 🔴 🔴 Database connection was failed! 🔴 🔴 🔴")
       print("Error:",error)
       time.sleep(3)

my_posts = [{"title": "first post", "content": "this is my first post", "id": 1}, {"title": "second post", "content": "this is my second post", "id": 2}]    


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i        
@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts= db.query(models.Post).all()
    return {"data": posts} 

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**new_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {
        "message": "Successfully created post!",
        "data": new_post,    
    }

@app.get("/posts/{id}")
def get_post(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {"data": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int,db: Session = Depends(get_db),):
    post =db.query(models.Post).filter(models.Post.id == id)

    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    # Fetch the updated post to return as response
    updated = post_query.first()

    return {"message": "Successfully updated post!", "data": updated}



@app.post("/user",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users",status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users= db.query(models.User).all()
    return {"data": users}