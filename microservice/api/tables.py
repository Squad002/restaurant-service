from microservice import db
from flask import Response
from flask.json import dumps
from connexion import request
from datetime import datetime
from microservice.models import Table, Restaurant


def post():
    request.get_data()
    table = request.json

    req_data = request.args
    new_table = db.session.query(Table.id).filter_by(name=table["name"]).first()

    q_res = db.session.query(Restaurant).filter_by(operator_id=req_data["operator_id"]).first()
    if q_res is None:
        return Response(status=403)
    
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

    q_res = db.session.query(Restaurant).filter_by(operator_id=req_data["operator_id"]).first()
    if q_res is None:
        return Response(status=403)

    if "seats" in req_data:
        print(req_data["seats"])
        query = db.session.query(Table).filter(
            Table.restaurant_id==req_data["restaurant_id"],
            Table.seats>=req_data["seats"]).order_by(Table.seats)
    else:
        query = db.session.query(Table).filter_by(restaurant_id=req_data["restaurant_id"])
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
    if not table:
        return Response(status=404)

    req_data = request.args
    q_res = db.session.query(Restaurant).filter_by(operator_id=req_data["operator_id"]).first()
    if q_res is None:
        return Response(status=403)

    return Response(
        dumps(
            table.serialize(
                [
                    "restaurant_id",
                    "name",
                    "seats",
                ]
            )
        ),
        status=200,
        mimetype="application/json",
    )


def patch(id):
    table_to_edit = db.session.query(Table).filter_by(id=id).first()
    if not table_to_edit:
        return Response(status=404)

    req_data = request.args
    in_table = request.json

    q_res = db.session.query(Restaurant).filter_by(operator_id=req_data["operator_id"]).first()
    if q_res is None:
        return Response(status=403)
    check_table = db.session.query(Table).filter(Table.name==in_table["name"], Table.id!=id).first()
    
    if not check_table:
        table_to_edit.name = in_table["name"]
        table_to_edit.seats = in_table["seats"]
        db.session.commit()

        return Response(status=204)
    else:
        return Response(status=400)


def delete(id):
    table_to_delete = db.session.query(Table).filter_by(id=id).first()
    if not table_to_delete:
        return Response(status=404)
    
    req_data = request.args
    q_res = db.session.query(Restaurant).filter_by(operator_id=req_data["operator_id"]).first()
    if q_res is None:
        return Response(status=403)

    db.session.delete(table_to_delete)
    db.session.commit()

    return Response(status=204)

