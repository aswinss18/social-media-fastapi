
from .. import models, schemas
from fastapi import  Depends, HTTPException, status,Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()  

@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts= db.query(models.Post).all()
    return {"data": posts} 

@router.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**new_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {
        "message": "Successfully created post!",
        "data": new_post,    
    }

@router.get("/posts/{id}")
def get_post(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {"data": post}

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int,db: Session = Depends(get_db),):
    post =db.query(models.Post).filter(models.Post.id == id)

    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
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

