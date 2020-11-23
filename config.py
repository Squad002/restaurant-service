import os
from logging import FileHandler, Formatter, StreamHandler, getLogger, INFO

logFormatter = Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
rootLogger = getLogger()

fileHandler = FileHandler("microservice.log", encoding="utf-8")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
""" 
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
fileHandler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
) """



class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "top secret"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///gooutsafe.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ELASTICSEARCH_URL=http://localhost:9200
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    @staticmethod
    def init_app(app):
        app.logger.addHandler(rootLogger)


class DevelopmentConfig(Config):

    DEBUG = True

    @staticmethod
    def init_app(app):
        # if I add logger here i got duplicate messages for errors and warnings
        app.debug = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///gooutsafe_test.db"
    )


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        rootLogger.setLevel(INFO)
        app.logger.addHandler(rootLogger)


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "docker": DockerConfig,
    "default": DevelopmentConfig,
}

mail_body_covid_19_mark = "Hey {},\nIn date {}, the health authority {} marked you positive to Covid-19. Contact your personal doctor to protect your health and that of others."
mail_body_covid_19_contact = "Hey {},\nIn date {}, while you were at restaurant {}, you could have been in contact with a Covid-19 case. Contact your personal doctor to protect your health and that of others."
mail_body_covid_19_operator_alert = "Hey {},\nIn date {}, at your restaurant {}, a Covid-19 case had a booking. Execute as soon as possible the health protocols."
mail_body_covid_19_operator_booking_alert = "Hey {},\nYou have a booking of a Covid-19 positive case, at your restaurant {}. The reservation ID is {} at table {}."