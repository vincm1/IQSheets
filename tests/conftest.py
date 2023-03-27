''' Testing configurations '''
import pytest
from config import config
from formelwizzard_app import create_app, db

# Fixture in Testing is availabel to every single test
@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.from_object(config['testing'])
    with app.app_context():
        yield app

@pytest.fixture(scope="module")
def client(app):
    return app.test_client()

@pytest.fixture(scope="module")
def _db(app):
    with app.app_context():
        db.create_all()
        yield db
        #db.session.remove()
        #db.drop_all()
