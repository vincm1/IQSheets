from formelwizzard_app.models import User
from flask_login import FlaskLoginClient

def test_home(client):
    # Send get request to homepage
    response = client.get('/')
    assert b'<meta charset="UTF-8" />' in response.data
    
# def test_registration(client, app, _db):
#     response = client.post('/register', data=dict(
#         username="vince",
#         email="vince@web.de",
#         password="Test123",
#         confirm="Test123"
#     ))

#     assert response.status_code == 200
    
#     # Extract user data from the response
#     with client.session_transaction() as session:
#         print(session)
#         user_id = session['user_id']
#         print(user_id)    
#     response_user = User.query.filter_by(id = user_id)

#     # Create a new user instance in the test database
#     test_user = User(
#         username=response_user.username,
#         email=response_user.email,
#         password=response_user.password
#     )
#     _db.session.add(test_user)
#     _db.session.commit()

#     assert User.query.count() == 1
#     assert User.query.filter_by(email="vince@web.de").first().email == response_user.email
    
def test_request_with_logged_in_user(client, app):
    app.test_client_class = FlaskLoginClient
    user = User.query.get(1)
    with app.test_client(user=user) as client:
        # This request has user 1 already logged in!
        client.get("/")
