from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users',]
)

### USER APIs

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.ResponseUser)
def create_user(user : schemas.CreateUser, db: Session = Depends(get_db)):
    #hash password = user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model= schemas.ResponseUser)
def get_users(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is not user with the {id} id")
    return user
