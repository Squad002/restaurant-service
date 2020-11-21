from microservice import db
from microservice.models import Operator
from flask import Response
from flask.json import dumps
from connexion import request
from datetime import datetime


def post():
    request.get_data()
    operator = request.json

    new_operator = (
        db.session.query(Operator.id).filter_by(email=operator["email"]).first()
    )
    if not new_operator:
        new_operator = Operator(
            firstname=operator["firstname"],
            lastname=operator["lastname"],
            email=operator["email"],
            password=operator["password"],
            birthdate=datetime.strptime(operator["birthdate"], "%Y-%m-%d"),
            phonenumber=operator["phonenumber"],
            fiscalcode=operator["fiscalcode"],
        )

        db.session.add(new_operator)
        db.session.commit()
        return Response(status=201)

    return Response(status=409)


def get(id):
    operator = db.session.query(Operator).filter_by(id=id).first()

    if operator:
        return Response(
            dumps(
                operator.serialize(
                    [
                        "id",
                        "firstname",
                        "lastname",
                        "email",
                        "fiscalcode",
                        "phonenumber",
                        "birthdate",
                    ]
                )
            ),
            status=200,
            mimetype="application/json",
        )

    return Response(status=404)


def patch(id):
    operator = db.session.query(Operator).filter_by(id=id).first()

    if operator:
        request.get_data()
        new_operator = request.json

        for k, v in new_operator.items():
            setattr(operator, k, v)

        db.session.commit()
        return Response(status=204)

    return Response(status=404)


def delete(id):
    operator = (
        db.session.query(Operator)
        .filter(Operator.id == id, Operator.email != "deleted")
        .first()
    )

    if operator:
        (
            operator.firstname,
            operator.lastname,
            operator.password_hash,
            operator.fiscalcode,
            operator.phonenumber,
            operator.birthdate,
            operator.email,
        ) = ("", "", "", "", "", None, "deleted")
        db.session.commit()
        return Response(status=204)

    return Response(status=404)
