from microservice import create_app, db
from microservice.services import mock
from microservice.models import Restaurant, Table, Menu, Food, Review 
from flask import request
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app, connexion_app = create_app(os.getenv("FLASK_CONFIG") or "default")
app.logger.info("Booting finished")


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    mock.everything()


@app.route("/testing/services/restaurant/db", methods=["GET", "DELETE"])
def delete_db():
    if request.method == "GET":
        return "Available", 204
    elif request.method == "DELETE":
        db.session.query(Restaurant).delete()
        db.session.query(Table).delete()
        db.session.query(Menu).delete()
        db.session.query(Food).delete()
        db.session.commit()

        return "OK", 204

    return "Error", 404