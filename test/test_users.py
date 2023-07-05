from fastapi import status
from app import schemas
from .database import client, session

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



