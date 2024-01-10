import pytest

from models import User, Post
from factory import db


@pytest.fixture(scope='function', autouse=True)
def clean_db():
    db.session.query(Post).delete()
    db.session.query(User).delete()
    db.session.commit()
