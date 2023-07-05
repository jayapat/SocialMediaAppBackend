from datetime import time
import os
from random import randrange
from typing import List, Optional
from httpx import ReadTimeout
import psycopg2
from pydantic import BaseModel
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Response,status
from psycopg2.extras import RealDictCursor
from . import oauth2, schemas

'''

app = FastAPI()
router = APIRouter(
    prefix="/posts",
    tags=['Posts',]
    )


app.include_router(router)

## pydantic is the library to define the schema. and it is the seperate library and nothing to do with the Fastapi
## lets say we want user to send the only two peace of the data. 1). title str and 2). content str

class post(BaseModel):
    title : str
    content : str
    published : bool = False
    rating : Optional[int] = None

## create database in memory
myposts = [{"title":"which is the longest river in the world?" , "content": "the longest river is nile", "published": True , "rating" : 5,"id":1},
           {"title":"what is the best programming language?" , "content": "offcourse, its python", "published": False , "rating" : 9, "id":2 },
           {"title":"what is the best car brand" , "content": "tata, the pride of india", "published": True, "id":3},
           {"title":"what is the best place in the world" , "content": "no doubt, its our home", "id":4}]

def get_post(id):
    for i in myposts:
        if i["id"] == id:
            return i
        
def get_deleted(id):
    for i,p in enumerate(myposts):
        if p["id"] == id:
            return i

@app.get("/") ##This is the decorator
# async def root(): ## Async is optional. It is only required when we have to perform the async tasks.
def root():
    return {"message": "this is forth api"} ## anytime you make the changes in the code, you have to restart the server. clt + c

## post request is to send some data to the api server. Then api server will talk with the databases and do whatever it is supposed to do.
## in return the api server send some data to the mobile device or the web application that, for ie successfully posted.

@app.post("/createposts")
def createpost():
    return {"message":"the post is successfully created"}


@app.post("/createpost")
def createpost(payload: dict = Body(...)):
    print(payload)
    return {"new post":f"title of the post is: {payload['title']}. And, the content of the post is {payload['content']}"}


@app.post("/createpost_class")
def createpost(new_post : post):
    print(new_post)
    return {"new_post is:":new_post.title,
            "published?":new_post.published}

## what is I make the mistake, lets try to send the int in the title
@app.post("/createpost_error")
def createpost(new_post : post):
    print(new_post)
    return {"new_post is:":new_post.title}

## publish
@app.post("/createpost_publish")
def createpost(new_post : post):
    print(new_post.published)
    return {"new_post is:":new_post.title, 
            "Post publised or not?": new_post.published,
            "rating":new_post.rating}

## Optional Rating
@app.post("/createpost_rating")
def createpost(new_post : post):
    print(new_post)
    print(new_post.dict()) ##pydantic has the method to convert into dict, .dict()
    return {"new_post is:":new_post.title, 
            "Post publised or not?": new_post.published,
            "rating":new_post.rating,
            "dict":new_post.dict()}

## as per the convention
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_post(post: post):
    posts = post.dict()
    posts["id"] = randrange(5,1000000000,1)
    myposts.append(posts)
    return {"data":posts}

@app.get("/posts")
def get_posts():
    return {"data":myposts}


@app.get("/posts/latest") ## Order matters, if I put this post second than the below next post, it will give an error.
def get_posts():
    return {"data": myposts[len(myposts) - 1]}

@app.get("/posts/{id}")
def get_posts(id : int): ## this autometically convert the id into the int; "response:Response" is not required with the rasie HTTPException
    if not get_post(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id {id} was not found") #HTTPException raise the error in the single lien
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message":f"post with the id {id} was not found"}
    return {"message":f"here is the post you are looking for {id}",
            "data":get_post(id)}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = get_deleted(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the id: {id} do not exist")
    myposts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

## put is used to change the entire entity and not just the single field.

@app.put("/posts/{id}")
def update_put_post(id : int, post : post):
    index = get_deleted(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"this post with the id {id} does not exist")
    posts = post.dict()
    posts["id"] = id
    myposts[index] = posts
    return {"updated post" : myposts[index]}


while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database='fastapi', 
                                user="postgres", password="2196", cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print(f"the error is {error}")
        time.sleep(3)


### Get post
@router.get("/", response_model=List[schemas.ResponsePost])
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    myposts = cursor.fetchall()
    print(myposts)
    return  myposts

    
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.ResponsePost)
def create_post(post : schemas.CreatePost, current_user : schemas.ResponseUser = Depends(oauth2.get_current_user)):
    cursor.execute(""" INSERT INTO posts (title, content, published, posts_users_id) VALUES (%s, %s, %s , %s) RETURNING * """,
                   (post.title, post.content, post.published, current_user.id))
    new_post = cursor.fetchone()
    conn.commit()
    return  new_post


### get individual post by id
@router.get("/{id}", response_model= schemas.ResponsePost)
def get_post(id : int):
    cursor.execute(f""" SELECT * FROM posts WHERE id = %s """,(str(id),))
    mypost = cursor.fetchone()
    if not mypost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"There is no post with the id = {id}")
    return mypost

### delete post

@router.delete("/{id}", response_model= schemas.ResponsePost)
def delete_post(id : int, current_user : schemas.ResponseUser = Depends(oauth2.get_current_user)):
    cursor.execute("""DELETE FROM posts WHERE id = %s and posts_users_id = %s RETURNING * """,(str(id),str(current_user.id),))
    deleted_post = cursor.fetchone() 
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"There is no post with {id} id")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.ResponsePost)
def update_post(id : int, post : schemas.UpdatePost, current_user : schemas.ResponseUser = Depends(oauth2.get_current_user)):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s and posts_users_id = %s RETURNING * """, 
                   (post.title, post.content,post.published, str(id), str(current_user.id),))
    replaced_post = cursor.fetchone()
    conn.commit()
    if not replaced_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"there is no post witht the id {id} to replace")
    return replaced_post


# How to extract the environment variable in python
Path = os.getenv("Path")
print(Path)

'''