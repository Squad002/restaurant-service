from microservice import db
from .restaurant import restaurantprecautions


class Precaution(db.Model):
    __tablename__ = "precaution"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(100))

    restaurant = db.relationship("Restaurant", secondary=restaurantprecautions, back_populates="precautions")
