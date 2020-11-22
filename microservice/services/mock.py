import datetime

from microservice import db
from microservice.models import (
    Restaurant,
    Precaution,
    Menu,
    Table,
    Review,
    Food
)


def everything():
    precaution()
    restaurant()
    table()
    menu()
    review()


def restaurant():
    q = db.session.query(Restaurant).filter(Restaurant.id == 1)
    restaurant = q.first()
    if restaurant is None:
        rest = Restaurant(
            name="Spaghetteria L'Archetto",
            phone=555123456,
            lat=43.720586,
            lon=10.408347,
            operator_id=1,
            time_of_stay=30,
            cuisine_type="ETHNIC",
            opening_hours=12,
            closing_hours=24,
        )
        precautions = db.session.query(Precaution).all()
        for precaution in precautions:
            rest.precautions.append(precaution)
        db.session.add(rest)

        rest = Restaurant(
            name="Pizzeria Italia dal 1987",
            phone=555123456,
            lat=44.720586,
            lon=10.408347,
            operator_id=1,
            time_of_stay=90,
            cuisine_type="FAST_FOOD",
            opening_hours=0,
            closing_hours=24,
        )
        precautions = db.session.query(Precaution).all()
        for precaution in precautions:
            rest.precautions.append(precaution)
        db.session.add(rest)

        rest = Restaurant(
            name="Ristorante Pizzeria Golfo di Napoli",
            phone=555123456,
            lat=43.720586,
            lon=9.408347,
            operator_id=1,
            time_of_stay=180,
            cuisine_type="PUB",
            opening_hours=19,
            closing_hours=5,
        )
        precautions = db.session.query(Precaution).all()
        for precaution in precautions:
            rest.precautions.append(precaution)
        db.session.add(rest)

        db.session.commit()


def precaution():
    q = db.session.query(Precaution).filter(Precaution.id == 1)
    precautions = q.first()
    if precautions is None:
        db.session.add(Precaution(name="Amuchina"))
        db.session.add(Precaution(name="Social distancing"))
        db.session.add(Precaution(name="Disposable menu"))
        db.session.add(Precaution(name="Personnel required to wash hands regularly"))
        db.session.add(Precaution(name="Obligatory masks for staff in public areas"))
        db.session.add(Precaution(name="Tables sanitized at the end of each meal"))

        db.session.commit()


def table():
    q = db.session.query(Table).filter(Table.restaurant_id == 1)
    table = q.first()
    if table is None:
        db.session.add(Table(name="1", seats=5, restaurant_id=1))
        db.session.add(Table(name="2", seats=3, restaurant_id=1))
        db.session.add(Table(name="3", seats=3, restaurant_id=1))
        db.session.add(Table(name="4", seats=6, restaurant_id=1))
        db.session.add(Table(name="1", seats=10, restaurant_id=2))
        db.session.add(Table(name="2", seats=3, restaurant_id=2))
        db.session.add(Table(name="1", seats=2, restaurant_id=3))
        db.session.add(Table(name="2", seats=2, restaurant_id=3))
        db.session.commit()


def review():
    review = db.session.query(Review).first()
    if review is None:
        db.session.add(
            Review(
                user_id=1,
                restaurant_id=1,
                rating=5,
                message="Ottimo Ristorante, il prezzo è gisto e i piatti sono gustosi. Ci tornerò sicuramente con la mia famiglia!",
            )
        )
        db.session.add(
            Review(
                user_id=2,
                restaurant_id=1,
                rating=1,
                message="Pessimo ristorante, il servizio è lento e i prezzo è eccessivo!",
            )
        )
        db.session.add(
            Review(
                user_id=3,
                restaurant_id=1,
                rating=5,
                message="Cucina veramente ottima e personale super gentile, a breve ci tornerò sicuramente!",
            )
        )
        db.session.add(
            Review(
                user_id=1,
                restaurant_id=2,
                rating=5,
                message="Primi sempre eccellenti, qualità prezzo imbattibile in zona. I tavoli solo esterni con un servizio sempre all’altezza",
            )
        )
        db.session.add(
            Review(
                user_id=2,
                restaurant_id=2,
                rating=3,
                message="Questo ristorante era proprio sotto il nostro appartamento, abbiamo sia pranzato che cenato. La pasta fatta molto bene e anche la pizza romana buona, personale molto gentile, prezzi nella media.",
            )
        )
        db.session.add(
            Review(
                user_id=3,
                restaurant_id=2,
                rating=5,
                message="Cucina veramente ottima e personale super gentile, a breve ci tornerò sicuramente!",
            )
        )
        db.session.add(
            Review(
                user_id=1,
                restaurant_id=3,
                rating=4,
                message="a me non piace la pizza a taglio (preferisco quella tonda) ma qui la fanno veramente buona gustosa e facile da digerire",
            )
        )
        db.session.add(
            Review(
                user_id=2,
                restaurant_id=3,
                rating=5,
                message="Situato in pieno centro storico di Roma. Personale molto gentile e simpatico, pizza buonissima, consiglio assolutamente",
            )
        )
        db.session.add(
            Review(
                user_id=3,
                restaurant_id=3,
                rating=5,
                message="Cucina veramente ottima e personale super gentile, a breve ci tornerò sicuramente!",
            )
        )
        db.session.commit()


def menu():
    q = db.session.query(Menu).filter(Menu.restaurant_id == 1)
    menu = q.first()
    if menu is None:
        menu = Menu(name="Trial Menu", restaurant_id=1)
        menu.foods.append(Food(name="Pepperoni pizza", price=5, category="PIZZAS"))
        menu.foods.append(Food(name="Water bottle", price=2, category="DRINKS"))

        db.session.add(menu)
        db.session.commit()