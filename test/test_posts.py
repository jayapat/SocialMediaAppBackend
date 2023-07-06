# To test whether are we getting the all the post
def test_get_all_posts(authorised_client, create_post):
    res = authorised_client.get("/posts/sqlalchemy")
    print(res.json())
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
    assert res.status_code == 201

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
