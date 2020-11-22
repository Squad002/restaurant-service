from microservice import db
import enum


menuitems = db.Table(
    "menuitems",
    db.Column("menu_id", db.Integer, db.ForeignKey("menu.id"), primary_key=True),
    db.Column("food_id", db.Integer, db.ForeignKey("food.id"), primary_key=True),
)


class FoodCategory(enum.Enum):
    STARTERS = "Starters"
    MAIN_COURSES = "Main Courses"
    SIDE_DISHES = "Side Dishes"
    DESSERTS = "Desserts"
    DRINKS = "Drinks"
    PIZZAS = "Pizzas"
    BURGERS = "Burgers"
    SANDWICHES = "Sandwiches"


class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text(100))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"))

    restaurant = db.relationship("Restaurant", back_populates="menus")
    foods = db.relationship("Food", secondary=menuitems, back_populates="menu")

    def serialize_menu(self):
        foods = []
        if self.foods:
            foods = [food.serialize_food() for food in self.foods]
        return {
            "id" : self.id,
            "name" : self.name,
            "foods" : foods,
            "restaurant_id" : self.restaurant_id,
        }


class Food(db.Model):
    __tablename__ = "food"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    category = db.Column(db.Enum(FoodCategory))
    name = db.Column(db.Text(100))
    price = db.Column(db.Float)

    menu = db.relationship("Menu", secondary=menuitems, back_populates="foods")

    def serialize_food(self):
        return{
            "category" : self.category.name,
            "name" : self.name,
            "price" : self.price,
        }
