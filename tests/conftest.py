from datetime import date

import pytest
from flask_jwt_extended import create_access_token

from factory import db
from models import User
from main import create_app


@pytest.fixture(scope='module')
def test_client():
    client = create_app("config.TestingConfig")

    with client.test_client() as testing_client:
        with client.app_context():
            yield testing_client


@pytest.fixture()
def seed_db():
    user = User(
        username="neville_bg",
        email="neville_bg@hotmail.com",
        birthdate=date.fromisoformat("1998-01-21"),
        password='1234@1234'
    )
    db.session.add(user)
    db.session.commit()

    yield user


@pytest.fixture()
def access_token():
    user = User.query.filter_by(username='neville_bg').first()

    token = create_access_token(identity=user.id)

    return {'Authorization': f'Bearer {token}'}
