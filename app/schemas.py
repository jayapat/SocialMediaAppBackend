from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, conint

### Post Post
class Post(BaseModel):
    title : str
    content : str
    published : bool = True

class CreatePost(Post):
    pass

class UpdatePost(Post):
    pass

class ResponseUser(BaseModel):
    email : EmailStr
    id : int
    created_at : datetime

    class Config:
        orm_mode = True

### Contol what response we want to send
class ResponsePost(Post):
    id : int
    created_at : datetime
    posts_users_id : int
    owner : ResponseUser

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email : EmailStr
    password : str


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token :str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir : int = Field(e= 0, le = 1)
    
class postVOTE(BaseModel):
    Post: Optional[ResponsePost]
    Vote: Optional[int]
    class Config:
        orm_mode = True
