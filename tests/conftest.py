''' Testing configurations '''
import pytest
from config import config
from flask_login import FlaskLoginClient
from iqsheets_app import create_app, db
from iqsheets_app.models import User

# Fixture in Testing is availabel to every single test
@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.from_object(config['testing'])
    app.test_client_class = FlaskLoginClient
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
        db.session.remove()
        db.drop_all()

def test_request_with_logged_in_user(app):
    user = User(email="test@example.com", password="password")
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    # Anmeldung des Testbenutzers und Durchführung des Tests
    with app.test_client(user=user) as client:
        response = client.get("/")
        assert response.status_code == 200