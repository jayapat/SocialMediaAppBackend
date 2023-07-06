from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app import models
from app.config import settings
from app.database import get_db, Base
from app.main import app
from sqlalchemy.orm import sessionmaker
import pytest 
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocaTest = sessionmaker(autocommit = False,autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocaTest()
    try:
        yield db
    finally:
        db.close()      

@pytest.fixture() 
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def create_user(client):
    user_data = {"email":"jay@gmail.com", "password":"12345"}
    res = client.post("/users", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = "12345"
    return new_user

@pytest.fixture()
def token(create_user):
    return create_access_token({"user_id":create_user["id"]})

@pytest.fixture()
def authorised_client(client, token):
    client.headers = {
        **client.headers,"Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture()
def create_post(create_user, session):
    post_data = [{
    "title" : "this is my which post?",
    "content": "this is my first post",
    "posts_users_id": create_user["id"]},
    {"title" : "which city you live in?",
    "content": "I live in Dallas",
    "posts_users_id" : create_user["id"]},
    {"title" : "this is my which post?",
    "content": "this is my Second post",
    "posts_users_id": create_user["id"]}]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    session.add_all(posts)

    session.commit()

    posts = session.query(models.Post).all()

    return posts