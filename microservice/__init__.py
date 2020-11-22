from connexion.resolver import RestyResolver
from flask_sqlalchemy import SQLAlchemy
from config import config

import connexion
import os.path

db = SQLAlchemy()


def create_app(config_name, updated_variables=None):
    connexion_app = connexion.App(__name__, specification_dir="../")

    # Get the underlying Flask app instance and put config in it
    flask_app = connexion_app.app
    flask_app.config.from_object(config[config_name])

    if updated_variables:
        flask_app.config.update(updated_variables)

    config[config_name].init_app(flask_app)
    context = flask_app.app_context()
    context.push()

    # Database init
    from microservice.models import Restaurant, Table, Food, Menu, Review, SearchableMixin, TimestampMixin, Precaution

    db.init_app(flask_app)
    db.create_all(app=flask_app)

    if not os.path.isfile("./gooutsafe.db"):
        for precaution in precautions:
            db.session.add(Precaution(name=precaution["name"]))

        db.session.commit()

    # Load APIs
    connexion_app.add_api("openapi.yml", resolver=RestyResolver("microservice.api"))
    flask_app.logger.info("Booting up")

    return flask_app, connexion_app

precaution1 = dict(name="Amuchina")
precaution2 = dict(name="Social distancing")
precaution3 = dict(name="Disposable menu")
precaution4 = dict(name="Personnel required to wash hands regularly")
precaution5 = dict(name="Obligatory masks for staff in public areas")
precaution6 = dict(name="Tables sanitized at the end of each meal")
precautions = [
    precaution1,
    precaution2,
    precaution3,
    precaution4,
    precaution5,
    precaution6,
]