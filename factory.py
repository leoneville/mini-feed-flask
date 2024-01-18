from flask import Flask
from config import BLACKLIST
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from spectree import SpecTree, SecurityScheme

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
api = SpecTree(
    'flask',
    title='Mini Feed API',
    version='v.1.0',
    path='docs',
    security_schemes=[
        SecurityScheme(
            name='api_key',
            data={'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}
        )
    ],
    security={'api_key': []}
)


def create_app(config_class: object | str):
    app = Flask(__name__)
    app.config.from_object(config_class)

    jwt.init_app(app)

    db.init_app(app)

    from models import User, Post
    migrate.init_app(app, db)

    from controllers.routes import initialize_routes
    initialize_routes(app)

    api.register(app)

    @jwt.token_in_blocklist_loader
    def revoked_token(header, payload):
        return payload['jti'] in BLACKLIST

    @jwt.expired_token_loader
    def expired_token(header, payload):
        return {'msg': 'Token expirado.'}, 401

    @jwt.invalid_token_loader
    def invalid_token(error):
        return {'msg': 'Token inválido.'}, 401

    @jwt.revoked_token_loader
    def revoked_token(header, payload):
        return {'msg': 'Token revogado.'}, 401

    @jwt.user_lookup_loader
    def user_load(header, payload):
        current_user = db.session.get(User, payload['sub'])

        return current_user

    return app
