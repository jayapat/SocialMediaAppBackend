
from fastapi import FastAPI
from . import models
from .database import engine
#models.Base.metadata.create_all(bind=engine) -- if not alembic then we can use this to generate the table from the sqlalchemy
from .routers import post, user, auth, votes
from .config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() ## We have created the instance #app - ocject

origins = ["*"]

app.add_middleware(
    CORSMiddleware,  #middle ware is the function which run before api route to the routers and perform some sort of operations.
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #only specific methods, for example get
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return "Hello World!"
