from fastapi import status
from jose import jwt
from app import schemas
from app.config import settings
import pytest

# Testing of the Testing :)
def test_root(client):
    res = client.get("/",)
    print(res.json())
    assert res.json() == "Hello World!"
    assert res.status_code == status.HTTP_200_OK

# Creating user testing, do we able to create user properly
def test_create_user(client):
    res = client.post("/users", json= {"email" : "hello3@gmail.com", "password" : "12345"})
    new_user = schemas.ResponseUser(**res.json())
    assert new_user.email == "hello3@gmail.com"
    assert res.status_code == status.HTTP_201_CREATED

#do we able to log in properly
def test_login(client, create_user):
    res = client.post("/login", data= {"username" : create_user["email"], "password" : create_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms= settings.algorithm)
    id = payload.get("user_id")
    assert id == create_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == status.HTTP_200_OK

# if we provide the wrong password, wrong email, are we getting the errors which we are supposed to
@pytest.mark.parametrize("email,password,status_code",[
    ("jasg@ggsgw.com","aettrae",403),
    ("etwtrwfew@srgetht.com","12345",403),
    ("jay@gmail.com",None,422)
])
def test_incorrect_login(create_user, client,email, password, status_code):
    res = client.post("/login", data= {"username" : email, "password" : password})
    assert res.status_code == status_code


