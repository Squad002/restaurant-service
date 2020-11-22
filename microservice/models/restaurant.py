from microservice import db
from microservice.models.searchable_mixin import SearchableMixin
from .table import Table
import enum
import datetime

restaurantprecautions = db.Table('restaurantprecautions',
    db.Column('precaution_id', db.Integer, db.ForeignKey('precaution.id'), primary_key=True),
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
)


class CuisineType(enum.Enum):
    ETHNIC = "Ethnic"
    FAST_FOOD = "Fast Food"
    PUB = "Pub"


#TODO add elastic search SearchableMixin
class Restaurant(db.Model):
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

    precautions = db.relationship("Precaution", secondary=restaurantprecautions, back_populates="restaurant")
    tables = db.relationship("Table", back_populates="restaurant")
    reviews = db.relationship("Review", back_populates="restaurant")
    menus = db.relationship("Menu", back_populates="restaurant")

    def serialize(self, keys):
        return {
            "id" : self.id,
            "name" : self.name,
            "phone" : self.phone,
            "lat" : self.lat,
            "lon" : self.lon,
            "time_of_stay" : self.time_of_stay,
            "cuisine_type" : self.cuisine_type.name,
            "opening_hours" : self.opening_hours,
            "closing_hours" : self.closing_hours,
            "operator_id" : self.operator_id,
            "average_rating" : self.average_rating,
            "precautions" : [precaution.name for precaution in self.precautions]
        }
