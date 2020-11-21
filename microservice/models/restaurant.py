from microservice import db
from microservice.models.searchable_mixin import SearchableMixin
from .table import Table
import enum
import datetime

precautions = db.Table('precautions',
    db.Column('precaution_id', db.Integer, db.ForeignKey('precaution.id'), primary_key=True),
    db.Column('restaurant', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
)


class CuisineType(enum.Enum):
    ETHNIC = "Ethnic"
    FAST_FOOD = "Fast Food"
    PUB = "Pub"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


class Restaurant(SearchableMixin, db.Model):
    __tablename__ = "restaurant"
    __searchable__ = ["name", "phone", "average_rating"]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text(100))

    lat = db.Column(db.Float)  # restaurant latitude
    lon = db.Column(db.Float)  # restaurant longitude

    phone = db.Column(db.Unicode(40))
    time_of_stay = db.Column(db.Integer)  # minutes
    cuisine_type = db.Column(db.Enum(CuisineType))
    opening_hours = db.Column(db.Integer)
    closing_hours = db.Column(db.Integer)
    operator_id = db.Column(db.Integer)
    average_rating = db.Column(db.Integer, default=0)

    precautions = db.relationship("Precaution", secondary=precautions, back_populates="restaurant")
    tables = db.relationship("Table", back_populates="restaurant")
    reviews = db.relationship("Review", back_populates="restaurant")
    menus = db.relationship("Menu", back_populates="restaurant")
