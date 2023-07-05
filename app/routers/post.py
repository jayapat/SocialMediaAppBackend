from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas,oauth2
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts',]
    )
#MongoDB - Mongoos


## For the Test on the SQLAlchemy
@router.get("/sqlalchemy", response_model=List[schemas.postVOTE])
def Get_Posts_SQLAlchemy(db : Session = Depends(get_db), limit : int = None, offset : int = None, search : Optional[str] = ""):
    results = db.query(models.Post, func.count(models.Vote.post_id).
                       label("Vote")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                                                                         isouter=True).group_by(models.Post.id).order_by(models.Post.id).filter(models.Post.title.contains(search)).offset(offset).limit(limit).all()
    return results


@router.post("/sqlalchemy", status_code=status.HTTP_201_CREATED, response_model= schemas.ResponsePost)
def post_sqlalchemy( post : schemas.CreatePost, db : Session = Depends(get_db), current_user : schemas.ResponseUser = Depends(oauth2.get_current_user)):
    new_post = models.Post(posts_users_id = current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/sqlalchemy/{id}", response_model= schemas.postVOTE)
def get_post_sqlalchemy(id:int, db : Session = Depends(get_db)):
    results = db.query(models.Post, func.count(models.Vote.post_id).
                       label("Vote")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                           isouter=True).filter(models.Post.id == id).group_by(models.Post.id).order_by(models.Post.id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"there is no post with {id} id")
    return results

@router.delete("/sqlalchemy/{id}", response_model= schemas.ResponsePost)
def delete_post_sqlalchemy(id:int, db : Session = Depends(get_db), current_user : schemas.ResponseUser = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"there is no post with {id} id")
    
    if post.first().posts_users_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user is not allowed to delete the post")

    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  

@router.put("/sqlalchemy/{id}",status_code=status.HTTP_202_ACCEPTED, response_model= schemas.ResponsePost)
def update_post_sqlalchemy(post : schemas.UpdatePost, id:int, db : Session = Depends(get_db), current_user : schemas.ResponseUser = Depends(oauth2.get_current_user)):
    updated_post = post.dict()
    update_query = db.query(models.Post).filter(models.Post.id == id)
    if not update_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is not post with the {id} id")
    
    if update_query.first().posts_users_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user is not allowed to update the post")
    update_query.update(updated_post)
    db.commit()
    return update_query.first()
    