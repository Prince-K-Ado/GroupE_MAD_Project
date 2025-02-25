import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import create_app

@pytest.fixture
def client():
    
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_success(client):
    response = client.post('/login', data={
        'email': 'user@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert b"Welcome back" in response.data

def test_login_failure(client):
    response = client.post('/login', data={
        'email': 'user@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b"Invalid credentials" in response.data
