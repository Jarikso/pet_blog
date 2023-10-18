from pathlib import Path


def test_create_user(new_user):
    assert new_user.id == 10
    assert new_user.name == "TestName"
    assert new_user.token == "testtoken"


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_access_token(client):
    response_not_token = client.get("/api/users/me", headers="")
    assert response_not_token.status_code == 400
    assert response_not_token.json["result"] is False
    response_not_token_db = client.get("/api/users/me",
                                       headers={"api-key": "test-bad"})
    assert response_not_token_db.status_code == 400
    assert response_not_token.json["result"] is False


def test_home_page_post(client):
    response = client.post("/")
    assert response.status_code == 405


def test_api_get_person_data(client, header):
    response = client.get("/api/users/me", headers=header)
    assert response.status_code == 200
    assert response.json["user"]["name"] == "jarikson"


def test_api_get_user_data(client, header):
    response = client.get("/api/users/1", headers=header)
    assert response.status_code == 200
    assert response.json["user"]["name"] == "jarikson"


def test_api_add_follow(client, header):
    response = client.post("/api/users/1/follow", headers=header)
    assert response.status_code == 200
    assert response.json["result"] is True


def test_api_delete_follow(client, header):
    response = client.post("/api/users/1/follow", headers=header)
    assert response.status_code == 200
    assert response.json["result"] is True


def test_api_list_tweets(client):
    response = client.get("/api/tweets")
    assert response.status_code == 200
    assert response.json["result"] is True


def test_api_add_and_delete_tweet(client, header):
    new_tweet = {"tweet_data": "test text",
                 "tweet_media_ids": [], "user_id": 10}
    new_tweet_response = client.post("/api/tweets",
                                     headers=header, json=new_tweet)
    assert new_tweet_response.status_code == 200
    assert new_tweet_response.json["result"] is True
    tweet_id = new_tweet_response.json["tweet_id"]
    del_tweet_response = client.delete(f"/api/tweets/{tweet_id}",
                                       headers=header)
    assert del_tweet_response.status_code == 200


def test_add_image(client, header):
    resources = Path(__file__).parent / "resources"
    response = client.post(
        "/api/medias",
        headers=header,
        data={"file": (resources / "test_image.png").open("rb")},
    )
    assert response.status_code == 200


def test_api_add_like(client, header):
    add_response = client.post("/api/tweets/1/likes", headers=header)
    assert add_response.status_code == 200
    assert add_response.json["result"] is True


def test_api_delete_like(client, header):
    del_response = client.post("/api/tweets/1/likes", headers=header)
    assert del_response.status_code == 200
    assert del_response.json["result"] is True
