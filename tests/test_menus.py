from tests.fixtures import app, client, db

from microservice.models import Menu


def test_post_should_add_menu(client, db):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    res = client.post(
        "/menus",
        json=menu,
    )
    
    db_menu = db.session.query(Menu).filter_by(name=menu["name"]).first()
    assert db_menu.name == menu["name"]
    assert res.status_code == 201


def test_post_should_not_add_menu(client):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    # first post to create menu
    client.post(
        "/menus",
        json=menu,
    )

    # recreating the same menu again
    res = client.post(
        "/menus",
        json=menu,
    )

    assert res.status_code == 409


def test_search(client):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/menus",
        json=menu,
    )

    res = client.get(
        "/menus?id=1",
    )

    assert res.status_code == 200

    rcv_menu = res.json
    assert rcv_menu[0]["id"] == 1
    assert rcv_menu[0]["name"] == menu["name"]
    assert rcv_menu[0]["foods"] == menu["foods"]
    assert rcv_menu[0]["restaurant_id"] == menu["restaurant_id"]


def test_get_should_work(client):
    client.post(
        "/restaurants",
        json=restaurant,
    )

    client.post(
        "/menus",
        json=menu,
    )

    res = client.get(
        "/menus/1",
    )

    assert res.status_code == 200

    rcv_menu = res.json
    assert rcv_menu["id"] == 1
    assert rcv_menu["name"] == menu["name"]
    assert rcv_menu["foods"] == menu["foods"]
    assert rcv_menu["restaurant_id"] == menu["restaurant_id"]


def test_get_should_not_work(client):

    # in case no menu with this id has been posted
    res = client.get(
        "/menus/1",
    )

    assert res.status_code == 404


menu = dict(
    name="Trial Menu",
    foods=[{
        "category" : "STARTERS",
        "name" : "Pepperoni pizza",
        "price" : 5.6,
    }],
    restaurant_id=1
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