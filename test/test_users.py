from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.config import settings
from app.database import get_db, Base
from app.main import app
from fastapi import status
from app import models, schemas
from sqlalchemy.orm import sessionmaker, declarative_base
import pytest 

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

testing_SessionLocal = sessionmaker(autocommit = False,autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture #yield gives us the flexibilty to run our code before and after the out test run
def client():
    yield TestClient(app)
    

def test_root(client):
    res = client.get("/",)
    print(res.json())
    assert res.json() == "Hello World!"
    assert res.status_code == status.HTTP_200_OK

def test_create_user(client):
    res = client.post("/users", json= {"email" : "hello3@gmail.com", "password" : "12345"})
    new_user = schemas.ResponseUser(**res.json())
    assert new_user.email == "hello3@gmail.com"
    assert res.status_code == status.HTTP_201_CREATED



