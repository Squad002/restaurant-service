from tests.fixtures import app, client, db

from microservice.models import Table


def test_search_should_return_results(client):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/tables?operator_id=1",
        json=table,
    )

    res = client.get("/tables?operator_id=1&restaurant_id=1")

    assert res.status_code == 200
    assert res.json[0]["name"] == table["name"]
    assert res.json[0]["seats"] == table["seats"]


def test_search_should_return_empty_results(client):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/tables?operator_id=1",
        json=table,
    )

    res = client.get("/tables?operator_id=1&restaurant_id=234234")

    assert res.status_code == 200
    assert res.json == []


def test_post_should_be_successful(client, db):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    res = client.post(
        "/tables?operator_id=1",
        json=table,
    )

    q = db.session.query(Table).filter_by(id=1).first()

    assert res.status_code == 201
    assert q.name == table["name"]
    assert q.seats == table["seats"]
    assert q.restaurant_id == table["restaurant_id"]


def test_post_should_be_unsuccessful(client, db):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/tables?operator_id=1",
        json=table,
    )

    res = client.post(
        "/tables?operator_id=1",
        json=table,
    )

    assert res.status_code == 409


def test_get_should_return_table(client):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/tables?operator_id=1",
        json=table,
    )

    res = client.get("/tables/1?operator_id=1")

    assert res.status_code == 200
    assert res.json["name"] == table["name"]
    assert res.json["seats"] == table["seats"]
    assert res.json["restaurant_id"] == table["restaurant_id"]


def test_get_should_not_return_table(client):
    res = client.get("/tables/1?operator_id=1")

    assert res.status_code == 404

    client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/tables?operator_id=1",
        json=table,
    )

    res = client.get("/tables/1?operator_id=1")

    assert res.status_code == 200
    assert res.json["name"] == table["name"]
    assert res.json["seats"] == table["seats"]
    assert res.json["restaurant_id"] == table["restaurant_id"]


def test_patch_should_be_successful(client, db):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/tables?operator_id=1",
        json=table,
    )

    res = client.patch("/tables/1?operator_id=1", json={"name": "A2", "seats": 20})
    q = db.session.query(Table).filter_by(id=1).first()

    assert res.status_code == 204
    assert q.name == "A2"
    assert q.seats == 20


def test_patch_should_not_be_successful(client, db):

    res = client.patch("/tables/1?operator_id=1", json={"name": "A2", "seats": 20})

    assert res.status_code == 404


def test_delete_should_be_successful(client, db):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/tables?operator_id=1",
        json=table,
    )

    res = client.delete("/tables/1?operator_id=1")

    assert res.status_code == 204


def test_delete_should_not_be_successful(client, db):
    res = client.delete("/tables/1?operator_id=1")

    assert res.status_code == 404



# Helpers

table = dict(
    name = "A1",
    seats = 10,
    restaurant_id = 1,
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
    operator_id=1,
)