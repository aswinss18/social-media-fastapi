from .. import models, schemas, utils,oauth2
from fastapi import  Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
       vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == get_current_user.id)
       found_vote = vote_query.first()
       if (vote.dir==1):
              if found_vote:
                  raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {get_current_user.id} has already voted on post {vote.post_id}")
              new_vote = models.Vote(post_id=vote.post_id, user_id=get_current_user.id)
              db.add(new_vote)
              db.commit()
              return {"message": "Successfully added vote!"}            

       else:
              if not found_vote:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
              
              vote_query.delete(synchronize_session=False)
              db.commit()
              
              return {"message": "Successfully deleted vote!"}