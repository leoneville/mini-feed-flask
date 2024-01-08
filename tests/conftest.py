from datetime import date

import pytest
from flask_jwt_extended import create_access_token

from models import User
from factory import db
from main import create_app


@pytest.fixture(scope='module')
def test_client():
    client = create_app("config.TestingConfig")

    with client.test_client() as testing_client:
        with client.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def access_token():
    user = User(
        username="test_user",
        email="test_user@hotmail.com",
        birthdate=date.fromisoformat("1998-01-21")
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)

    return {'Authorization': f'Bearer {token}'}
