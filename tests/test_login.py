# tests/test_login.py
import pytest
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # For tests, use an in-memory SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        # Create a test user
        test_user = User(email='test@example.com', password=generate_password_hash('password'))
        db.session.add(test_user)
        db.session.commit()
    client = app.test_client()
    yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_login_success(client):
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    assert b'Login successful!' in response.data

def test_login_failure(client):
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b'Invalid credentials' in response.data






# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# import pytest
# from GroupE.app import create_app

# @pytest.fixture
# def client():
    
#     app = create_app()
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client

# def test_login_success(client):
#     response = client.post('/login', data={
#         'email': 'user@example.com',
#         'password': 'password123'
#     }, follow_redirects=True)
#     assert b"Welcome back" in response.data

# def test_login_failure(client):
#     response = client.post('/login', data={
#         'email': 'user@example.com',
#         'password': 'wrongpassword'
#     }, follow_redirects=True)
#     assert b"Invalid credentials" in response.data
