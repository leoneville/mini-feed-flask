import pytest

from models import User
from factory import db


@pytest.fixture()
def seed_db():
    user = User(
        username='usuario_test',
        password='1234@1234',
        email='usuario_test@gmail.com'
    )

    db.session.add(user)
    db.session.commit()

    yield user


@pytest.fixture(autouse=True)
def clean_db():
    db.session.query(User).delete()
    db.session.commit()
