from tests.fixtures import app, client, db

from microservice.models import Restaurant, Precaution
from werkzeug.datastructures import FileStorage, MultiDict

def test_post_should_be_successful(client, db):
    db.session.add(Precaution(name="Amuchina"))
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
        json=restaurant2,
    )

    res = client.post(
        "/restaurants",
        json=restaurant,
    )

    assert res.status_code == 409


def test_get_should_return_restaurant(client):
    client.post(
        "/restaurants",
        json=restaurant2,
    )

    res = client.get("/restaurants/1")

    assert res.status_code == 200
    assert res.json["name"] == restaurant2["name"]
    assert res.json["lat"] == restaurant2["lat"]
    assert res.json["lon"] == restaurant2["lon"]
    assert res.json["phone"] == restaurant2["phone"]
    assert res.json["time_of_stay"] == restaurant2["time_of_stay"]
    assert res.json["opening_hours"] == restaurant2["opening_hours"]
    assert res.json["closing_hours"] == restaurant2["closing_hours"]
    assert res.json["operator_id"] == restaurant2["operator_id"]


def test_get_should_not_return_restaurant(client):
    res = client.get("/restaurants/1")

    assert res.status_code == 404


def test_search_should_return_results(client):
    client.post(
        "/restaurants",
        json=restaurant2,
    )

    res = client.get("/restaurants?id=1")

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
        json=restaurant2,
    )

    file_path = "./tests/pizza.jpg"
    file = FileStorage(open(file_path, "rb"), "pizza.jpg", content_type="image/jpg")
    files = MultiDict(
        [
            ("filename", file),
        ]
    )

    res = client.post("/restaurants/1/upload", data=files)

    assert res.status_code==201


def test_upload_should_not_work(client):
    file_path = "./tests/pizza.jpg"
    file = FileStorage(open(file_path, "rb"), "pizza.jpg", content_type="image/jpg")
    files = MultiDict(
        [
            ("filename", file),
        ]
    )

    res = client.post("/restaurants/1/upload", data=files)

    assert res.status_code==404


def test_patch_average_rating(client, db):
    client.post(
        "/restaurants",
        json=restaurant2,
    )

    client.post(
        "/reviews",
        json=review
    )

    res = client.patch(
        "/restaurants/1",
        json={"average_rating" : 1.5}
    )
    rest = db.session.query(Restaurant).filter_by(id=1).first()

    assert res.status_code == 204
    assert rest.average_rating == 1.5
    
    
def test_patch_average_rating_should_not_work(client, db):
    res = client.patch(
        "/restaurants/1",
        json={"average_rating" : 1.5}
    )

    assert res.status_code == 404
    

def test_permissions_ok(client):
    client.post(
        "/restaurants",
        json=restaurant2,
    )

    res = client.get(
        "/restaurants/1/permissions?operator_id=1"
    )

    assert res.status_code == 204


def test_permissions_ko(client):
    client.post(
        "/restaurants",
        json=restaurant2,
    )

    res = client.get(
        "/restaurants/1/permissions?operator_id=2"
    )

    assert res.status_code == 403


def test_permissions_not_found(client):
    res = client.get(
        "/restaurants/1/permissions?operator_id=1"
    )

    assert res.status_code == 404


restaurant = dict(
    name="Trattoria da Fabio",
    phone="555123456",
    lat=40.720586,
    lon=10.10,
    time_of_stay=30,
    cuisine_type="ETHNIC",
    precautions=["Amuchina"],
    opening_hours=12,
    closing_hours=18,
    operator_id=1,
)

restaurant2 = dict(
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

review = dict(
    rating=5,
    message="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    restaurant_id=1,
    user_id=1,
)
