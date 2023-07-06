def test_vote_on_post(authorised_client, create_post):
    res = authorised_client.post("/vote/", json = {"post_id": create_post[2].id, "dir" : 1})
    assert res.status_code == 201

def test_vote_on_post_twotime(authorised_client, create_post, lets_test_two_vote):
    res = authorised_client.post("/vote/", json = {"post_id": create_post[1].id, "dir" : 1})
    assert res.status_code == 409