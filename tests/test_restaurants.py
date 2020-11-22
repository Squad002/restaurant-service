from tests.fixtures import app, client, db

from microservice.models import Restaurant
from werkzeug.datastructures import FileStorage, MultiDict

def test_post_should_be_successful(client, db):
    res = client.post(
        "/restaurants",
        json=restaurant,
    )

    q = db.session.query(Restaurant).filter_by(id=1).first()

    assert res.status_code == 201
    assert q.name == restaurant["name"]
    assert q.lat == restaurant["lat"]
    assert q.lon == restaurant["lon"]
    assert q.phone == restaurant["phone"]
    assert q.time_of_stay == restaurant["time_of_stay"]
    assert q.opening_hours == restaurant["opening_hours"]
    assert q.closing_hours == restaurant["closing_hours"]
    assert q.operator_id == restaurant["operator_id"]


def test_post_should_be_unsuccessful(client, db):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    res = client.post(
        "/restaurants",
        json=restaurant,
    )

    assert res.status_code == 409


def test_get_should_return_restaurant(client):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    res = client.get("/restaurants/1")

    assert res.status_code == 200
    assert res.json["name"] == restaurant["name"]
    assert res.json["lat"] == restaurant["lat"]
    assert res.json["lon"] == restaurant["lon"]
    assert res.json["phone"] == restaurant["phone"]
    assert res.json["time_of_stay"] == restaurant["time_of_stay"]
    assert res.json["opening_hours"] == restaurant["opening_hours"]
    assert res.json["closing_hours"] == restaurant["closing_hours"]
    assert res.json["operator_id"] == restaurant["operator_id"]


def test_get_should_not_return_restaurant(client):
    res = client.get("/restaurants/1")

    assert res.status_code == 404


def test_search_should_return_results(client):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    res = client.get("/restaurants")

    assert res.status_code == 200
    assert res.json[0]["name"] == restaurant["name"]
    assert res.json[0]["lat"] == restaurant["lat"]
    assert res.json[0]["lon"] == restaurant["lon"]
    assert res.json[0]["phone"] == restaurant["phone"]
    assert res.json[0]["time_of_stay"] == restaurant["time_of_stay"]
    assert res.json[0]["opening_hours"] == restaurant["opening_hours"]
    assert res.json[0]["closing_hours"] == restaurant["closing_hours"]
    assert res.json[0]["operator_id"] == restaurant["operator_id"]


def test_upload(client):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    file_path = "./tests/pizza.jpg"
    file = FileStorage(open(file_path, "rb"), "pizza.jpg", content_type="image/jpg")
    files = MultiDict(
        [
            ("filename", file),
        ]
    )

    res = client.post("/restaurants/1/upload?operator_id=1", data=files)

    assert res.status_code==201

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