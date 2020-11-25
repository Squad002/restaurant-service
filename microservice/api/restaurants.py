from microservice import db
from flask import Response, current_app
from flask.json import dumps
from connexion import request
from datetime import datetime
from microservice.models import Restaurant
from werkzeug.datastructures import MultiDict
from flask import current_app

import os

logger = current_app.logger


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

        if "precautions" in restaurant:
            new_restaurant.precautions=','.join(restaurant["precautions"])

        db.session.add(new_restaurant)
        db.session.commit()
        os.makedirs("./microservice/static/uploads/" +
                    str(new_restaurant.id), exist_ok=True)

        return Response(status=201)

    return Response(status=409)


def search():
    request.get_data()
    req_data = request.args
    if "q" in req_data:
        # TODO fix better search
        restaurants = Restaurant.search(req_data["q"], int(req_data["page"]), int(req_data["perpage"]))
        restaurants = dumps([
                restaurant.serialize()
                for restaurant in restaurants[0].all()
            ])
    else:
        query = db.session.query(Restaurant)
        for attr, value in req_data.items():
            query = query.filter(getattr(Restaurant, attr) == value)

        restaurants = dumps(
            [
                restaurant.serialize()
                for restaurant in query.all()
            ]
        )

    return Response(restaurants, status=200, mimetype="application/json")


def get(id):
    restaurant = db.session.query(Restaurant).filter_by(id=id).first()
    if restaurant:
        return Response(
            dumps(restaurant.serialize()),
            status=200,
            mimetype="application/json",
        )

    return Response(status=404)


def upload(id):
    request.get_data()

    restaurant = db.session.query(Restaurant).filter_by(
        id=id).first()

    if restaurant:
        for key, uploaded_file in request.files.items():
            uploaded_file.save(os.path.join(
                "./microservice/static/uploads/" + str(id), uploaded_file.filename))

        return Response(status=201)

    return Response(status=404)


def patch(id): 
    restaurant = db.session.query(Restaurant).filter_by(id=id).first()
    
    if not restaurant:
        return Response(status=404)

    update = request.json

    restaurant.average_rating = update["average_rating"]
    db.session.commit()

    return Response(status=204)

