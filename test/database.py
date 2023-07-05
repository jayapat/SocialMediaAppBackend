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

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocaTest()
    try:
        yield db
    finally:
        db.close()      

@pytest.fixture #yield gives us the flexibilty to run our code before and after the out test run
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    