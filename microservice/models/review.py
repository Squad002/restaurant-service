from microservice import db
from .timestamp_mixin import TimestampMixin


class Review(TimestampMixin, db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant.id")
    )
    user_id = db.Column(db.Integer)

    restaurant = db.relationship("Restaurant", back_populates="reviews")

    rating = db.Column(db.SmallInteger, nullable=False)
    message = db.Column(db.UnicodeText)

    def serialize(self, keys):
        return dict([(k, v) for k, v in self.__dict__.items() if k in keys])