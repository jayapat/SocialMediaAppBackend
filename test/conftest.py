from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.config import settings
from app.database import get_db, Base
from app.main import app
from sqlalchemy.orm import sessionmaker
import pytest 

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
    