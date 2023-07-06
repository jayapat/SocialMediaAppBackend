# To test whether are we getting the all the post
from app import schemas


def test_get_all_posts(authorised_client, create_post):
    res = authorised_client.get("/posts/sqlalchemy")
    assert len(res.json()) == len(create_post)
    assert res.status_code == 200

# To test user is able to get the single post
def test_get_one_posts(authorised_client, create_post):
    res = authorised_client.get(f"/posts/sqlalchemy/{create_post[0].id}")
    assert res.status_code == 200

# To test if the id is not present than get an exception
def test_get_one_posts_which_not_exist(authorised_client, create_post):
    res = authorised_client.get(f"/posts/sqlalchemy/{create_post[-1].id+1000}")
    assert res.status_code == 404
    assert res.json()['detail'] == f"there is no post with {create_post[-1].id+1000} id"

# To test if the user is able to post
def test_do_post(authorised_client):
    res = authorised_client.post("/posts/sqlalchemy/",json= {"title" : "this is my which post?", "content": "this is my first post", "published" : False})
    created_post = schemas.Post(**res.json())
    print(created_post)
    assert res.status_code == 201
    assert created_post.title == "this is my which post?"

# to test if what user provide the wrong type in the published
def test_do_post(authorised_client):
    res = authorised_client.post("/posts/sqlalchemy/",json= {"title" : "this is my which post?", "content": "this is my first post", "published" : "abc"})
    assert res.status_code == 422
    

# to test if the unauthorized user able to post
def test_unauthorized_do_post(client):
    res = client.post("/posts/sqlalchemy/",json= {"title" : "this is my which post?", "content": "this is my first post", "published" : "abc"})
    assert res.status_code == 401
    assert res.json()['detail'] == "Not authenticated"
    

# to test if the authorized and current user able to delete the post
def test_unauthorized_delete_post(client,create_user,create_post):
    res = client.delete(f"/posts/sqlalchemy/{create_post[0].id}")
    assert res.status_code == 401


def test_authorized_delete_post(authorised_client,create_user,create_post):
    res = authorised_client.delete(f"/posts/sqlalchemy/{create_post[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorised_client,create_user,create_post):
    res = authorised_client.delete(f"/posts/sqlalchemy/10000")
    assert res.status_code == 404
    assert res.json()['detail'] == "there is no post with 10000 id"

def test_delete_other_users_post(authorised_client, create_post,create_user):
    res = authorised_client.delete(f"/posts/sqlalchemy/{create_post[2].id}")
    assert res.status_code == 403

def test_update_post(authorised_client,create_post,create_user):
    res = authorised_client.put(f"/posts/sqlalchemy/{create_post[1].id}",json= {"title" : "this is my which post?", "content": "this is my third post", "published" : False})
    assert res.status_code == 202

def test_others_update_post(authorised_client,create_post,create_user):
    res = authorised_client.put(f"/posts/sqlalchemy/{create_post[2].id}",json= {"title" : "this is my which post?", "content": "this is my third post", "published" : False})
    assert res.status_code == 403
