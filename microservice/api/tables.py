from microservice import db
from flask import Response
from flask.json import dumps
from connexion import request
from datetime import datetime
from microservice.models import Table


def post():
    request.get_data()
    table = request.json

    new_table = db.session.query(Table.id).filter_by(name=table["name"]).first()
    if not new_table:
        new_table = Table(
            name=table["name"],
            seats=table["seats"],
            restaurant_id=table["restaurant_id"],           
        )

        db.session.add(new_table)
        db.session.commit()
        return Response(status=201)

    return Response(status=409)


def search():
    request.get_data()
    req_data = request.args

    query = db.session.query(Table)
    for attr, value in req_data.items():
        query = query.filter(getattr(Table, attr) == value)

    tables = dumps(
        [
            table.serialize(
                [
                    "id",
                    "name",
                    "seats",
                    "restaurant_id",
                ]
            )
            for table in query.all()
        ]
    )

    return Response(tables, status=200, mimetype="application/json")


def get(id):
    table = db.session.query(Table).filter_by(id=id).first()

    if table:
        return Response(
            dumps(
                table.serialize(
                    [
                        "id",
                        "name",
                        "seats",
                    ]
                )
            ),
            status=200,
            mimetype="application/json",
        )

    return Response(status=404)


def patch(id):
    table_to_edit = db.session.query(Table).filter_by(id=id).first()

    in_table = request.json
    check_table = db.session.query(Table).filter(Table.name==in_table["name"], Table.id!=id).first()
    if table_to_edit:
        if not check_table:
            table_to_edit.name = in_table["name"]
            table_to_edit.seats = in_table["seats"]
            db.session.commit()

            return Response(status=204)
        else:
            return Response(status=400)


    return Response(status=404)


def delete(id):
    table_to_delete = db.session.query(Table).filter_by(id=id).first()

    if table_to_delete:
        db.session.delete(table_to_delete)
        db.session.commit()

        return Response(status=204)

    return Response(status=404)
