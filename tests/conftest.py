import pytest

from main import create_app


@pytest.fixture(scope='module')
def test_client():
    client = create_app("config.TestingConfig")

    with client.test_client() as testing_client:
        with client.app_context():
            yield testing_client
