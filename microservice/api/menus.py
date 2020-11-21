from microservice import db
from flask import Response
from flask.json import dumps
from connexion import request
from datetime import datetime
from microservice.models import Menu, Food



def post():
    request.get_data()
    new_menu = request.json
    print(new_menu)

    menu = db.session.query(Menu).filter_by(restaurant_id=new_menu["restaurant_id"],name=new_menu["name"]).first()

    if not menu:
        menu = Menu(
            name=new_menu["name"],
            restaurant_id=new_menu["restaurant_id"],
        )
        for food in new_menu["foods"]:
            foodie = Food(
                category=food["category"],
                name=food["name"],
                price=food["price"],
            )
            menu.foods.append(foodie)
        
        db.session.add(menu)
        db.session.commit()
        return Response(status=201)
    
    return Response(status=409)


def get(id):
    menu = db.session.query(Menu).filter_by(id=id).first()

    if menu:
        menu_dict = menu.serialize_menu()
        print(menu_dict)
        return Response(
            dumps(menu_dict),
            status=200,
            mimetype="application/json",
        )

    return Response(status=404)