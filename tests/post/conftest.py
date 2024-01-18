import pytest

from models import User, Post
from factory import db


@pytest.fixture(scope='function', autouse=True)
def clean_db(request):
    def teardown():
        db.session.query(Post).delete()
        db.session.query(User).delete()
        db.session.commit()

    request.addfinalizer(teardown)
