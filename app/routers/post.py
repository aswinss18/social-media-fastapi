
from .. import models, schemas
from fastapi import  Depends, HTTPException, status,Response, APIRouter
from sqlalchemy.orm import Session
from .. import oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["Posts"])  

@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user),limit: int = 10,skip: int = 0,search: Optional[str] = ""):
    posts= db.query(models.Post).filter((models.Post.owner_id == get_current_user.id) & models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return  posts

@router.get("/all",response_model=List[schemas.Post])
def get_all_posts(db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user),limit: int = 10,skip: int = 0,search:  Optional[str] = ""):
    posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return  posts

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_posts(new_post: schemas.CreatePost, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=get_current_user.id,**new_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {
        "message": "Successfully created post!",
        "data": new_post,    
    }

@router.get("/{id}",)
def get_post(id: int,db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    return {"data": post}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int,db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    post =db.query(models.Post).filter(models.Post.id == id)

    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    if post.first().owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )
    
    if post.first().owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    # Fetch the updated post to return as response
    updated = post_query.first()

    return {"message": "Successfully updated post!", "data": updated}

