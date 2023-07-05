from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas,oauth2, database
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix= "/vote",
    tags=["Vote", ]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db : Session = Depends(database.get_db), current_user : schemas.ResponseUser = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {vote.post_id} does not exist")

    vote_qurey = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_qurey.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"user {current_user.id} has already voted for the post {vote.post_id}")
        newvote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(newvote)
        db.commit()
        return {"message":"you have given the vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Vote does not exist")
        vote_qurey.delete()
        db.commit()
        return {"message":"vote successfuly deleted"}
    
        