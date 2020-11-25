from connexion.resolver import RestyResolver
from flask_sqlalchemy import SQLAlchemy
from config import config
from elasticsearch import Elasticsearch

import connexion

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

    # Elastic search init
    es_url = flask_app.config["ELASTICSEARCH_URL"]
    flask_app.elasticsearch = Elasticsearch([es_url]) if es_url else None

    # Database init
    from microservice.models import Restaurant, Table, Food, Menu, Review, SearchableMixin, TimestampMixin

    db.init_app(flask_app)
    db.create_all(app=flask_app)

    # Load APIs
    connexion_app.add_api("openapi.yml", resolver=RestyResolver("microservice.api"))
    flask_app.logger.info("Booting up")

    return flask_app, connexion_app
