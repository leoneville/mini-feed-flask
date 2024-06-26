import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
ACCESS_EXPIRES = timedelta(minutes=15)


class Config(object):
    JWT_TOKEN_LOCATION = ['headers']
    APP_TITLE = 'Flask REST API Course'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    @staticmethod
    def init_app(app):
        ...


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(basedir, "test_app.db")


class ProductionConfig(Config):
    uri = os.getenv("DATABASE_URL")

    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://")

    SQLALCHEMY_DATABASE_URI = uri
