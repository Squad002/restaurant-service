from microservice import db
from restaurant import precautions

class Precautions(db.Model):
    __tablename__ = "precautions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(100))

    restaurant = db.relationship("Restaurant", secondary=precautions, back_populates="precautions")
