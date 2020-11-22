from microservice import db
from flask import Response
from flask.json import dumps
from connexion import request
from datetime import datetime
from microservice.models import Restaurant, Precaution


def post():
    request.get_data()
    restaurant = request.json

    new_restaurant = db.session.query(Restaurant.id).filter_by(
        lat=restaurant["lat"], lon=restaurant["lon"]).first()
    if not new_restaurant:
        new_restaurant = Restaurant(
            name=restaurant["name"],
            lat=restaurant["lat"],
            lon=restaurant["lon"],
            phone=restaurant["phone"],
            time_of_stay=restaurant["time_of_stay"],
            cuisine_type=restaurant["cuisine_type"],
            opening_hours=restaurant["opening_hours"],
            closing_hours=restaurant["closing_hours"],
            operator_id=restaurant["operator_id"]
        )

        for precaution in restaurant["precautions"]:
            new_restaurant.precautions.append(Precaution(name=precaution))

        db.session.add(new_restaurant)
        db.session.commit()
        return Response(status=201)

    return Response(status=409)


def search():
    request.get_data()
    req_data = request.args

    query = db.session.query(Restaurant)
    for attr, value in req_data.items():
        query = query.filter(getattr(Restaurant, attr) == value)

    restaurants = dumps(
        [
            restaurant.serialize(restaurant)
            for restaurant in query.all()
        ]
    )

    return Response(restaurants, status=200, mimetype="application/json")


def get(id):
    restaurant = db.session.query(Restaurant).filter_by(id=id).first()

    if restaurant:
        return Response(
            dumps(restaurant.serialize(restaurant)),
            status=200,
            mimetype="application/json",
        )

    return Response(status=404)
