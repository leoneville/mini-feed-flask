from datetime import date

import pytest

from models import User
from factory import db


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
def seed_more_db():
    user = User(
        username="leoneville.dev",
        email="leoneville.dev@gmail.com",
        password='1234@1234'
    )
    db.session.add(user)
    db.session.commit()

    yield user


@pytest.fixture(scope='function', autouse=True)
def cleaning_db():
    db.session.query(User).delete()
    db.session.commit()
