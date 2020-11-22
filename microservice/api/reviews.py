from microservice import db
from flask import Response
from flask.json import dumps
from connexion import request
from datetime import datetime
from microservice.models import Restaurant, Review


def post():
    request.get_data()
    review = request.json

    print(review)
    restaurant = db.session.query(Restaurant.id).filter_by(id=review["restaurant_id"]).first()
    if restaurant:
        new_review = db.session.query(Review).filter_by(user_id=review["user_id"]).first()

        if not new_review:
            new_review = Review(
                restaurant_id=review["restaurant_id"],
                rating=review["rating"],
                message=review["message"],
            )

            db.session.add(new_review)
            db.session.commit()

            return Response(status=201)
        else:
            return Response(status=409)
    
    return Response(status=404)


def search():
    request.get_data()
    req_data = request.args

    query = db.session.query(Review)
    for attr, value in req_data.items():
        query = query.filter(getattr(Review, attr) == value)

    reviews = dumps(
        [
            review.serialize(
                [
                    "user_id",
                    "restaurant_id",
                    "restaurant",
                    "rating",
                    "message",
                ]
            )
            for review in query.all()
        ]
    )

    return Response(reviews, status=200, mimetype="application/json")