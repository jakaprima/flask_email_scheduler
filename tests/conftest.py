import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')  # Assume you have a testing configuration
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
        yield client  # Testing happens here
        with app.app_context():
            db.drop_all()  # Clean up after tests

@pytest.fixture
def celery_config():
    return {
        'broker_url': 'redis://127.0.0.1:6379/1',
        'result_backend': 'redis://127.0.0.1:6379/1',
    }