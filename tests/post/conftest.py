import pytest

from models import User, Post
from factory import db


@pytest.fixture()
def seed_post():
    posts = [
        {
            'text': 'texto do post 1',
            'author_id': 1
        },
        {
            'text': 'texto do post 2',
            'author_id': 99
        }
    ]

    posts_db = [Post(**post) for post in posts]

    db.session.add_all(posts_db)
    db.session.commit()


@pytest.fixture(scope='function', autouse=True)
def clean_db(request):
    def teardown():
        db.session.query(Post).delete()
        db.session.query(User).delete()
        db.session.commit()

    request.addfinalizer(teardown)
