from formelwizzard_app.models import User
from flask_login import FlaskLoginClient

def test_home(client):
    # Send get request to homepage
    response = client.get('/')
    assert b'<meta charset="UTF-8" />' in response.data
    
def test_registration(client):
    response = client.post('/register', data=dict(
                            username="vince_test", email="vince@test.de",
                            password="Test_PW123!", confirm_pw="Test_PW123!"),
                            follow_redirects=True)
    assert response.status_code == 200
    
def test_request_with_logged_in_user(client, app):
    app.test_client_class = FlaskLoginClient
    user = User.query.get(1)
    with app.test_client(user=user) as client:
        # This request has user 1 already logged in!
        client.get("/")
