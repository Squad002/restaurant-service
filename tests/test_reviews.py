from tests.fixtures import app, client, db

from microservice.models import Review


def test_search_should_return_results(client):
    res = client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/reviews",
        json=review,
    )

    res = client.get("/reviews?restaurant_id=1")

    assert res.status_code == 200
    assert res.json[0]["message"] == review["message"]


def test_search_should_return_empty_results(client):
    res = client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/reviews",
        json=review,
    )

    res = client.get("/reviews?restaurant_id=3324234")

    assert res.status_code == 200
    assert res.json == []


def test_post_should_be_successful(client, db):
    res = client.post(
        "/restaurants",
        json=restaurant,
    )
    
    res = client.post(
        "/reviews",
        json=review,
    )

    q = db.session.query(Review).filter_by(id=1).first()

    assert res.status_code == 201
    assert q.restaurant_id == review["restaurant_id"]
    assert q.rating == review["rating"]
    assert q.message == review["message"]


def test_post_should_be_unsuccessful(client, db):

    res = client.post(
        "/reviews",
        json=review,
    )

    assert res.status_code == 404

    res = client.post(
        "/restaurants",
        json=restaurant,
    )
    
    res = client.post(
        "/reviews",
        json=review,
    )
    assert res.status_code == 201
    
    res = client.post(
        "/reviews",
        json=review,
    )

    assert res.status_code == 409




# Helpers

review = dict(
    rating=5,
    message="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    restaurant_id=1,
    user_id=1,
)

restaurant = dict(
    name="Trattoria da Fabio",
    phone="555123456",
    lat=40.720586,
    lon=10.10,
    time_of_stay=30,
    cuisine_type="ETHNIC",
    opening_hours=12,
    closing_hours=18,
    precautions=["Amuchina"],
    operator_id=1,
)