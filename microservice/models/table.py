from microservice import db


class Table(db.Model):
    __tablename__ = "table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text(100))
    seats = db.Column(db.Integer)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"))

    restaurant = db.relationship("Restaurant", back_populates="tables")

    def serialize(self):
        return dict([(k,v) for k,v in self.__dict__.items() if k[0] != '_'])