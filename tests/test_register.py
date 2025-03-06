# tests/test_register.py
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from app.models import User
from sqlalchemy.orm import  scoped_session, sessionmaker
# from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture(scope='function')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MiniGoFundMe.db'
    
    ctx = app.app_context()
    ctx.push()
    
    db.create_all()
    
    connection = db.engine.connect()
    transaction = connection.begin()
    
    SessionFactory = sessionmaker(bind=connection)
    session = scoped_session(SessionFactory)
    db.session = session
    
    client = app.test_client()
    
    yield client
    
    session.remove()
    # transaction.rollback()
    # connection.close()
    # db.drop_all()
    # ctx.pop()

def test_register_success(client):
    response = client.post('/register', data={
        'email': 'newuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    
    # Check that the registration flash message is in the response.
    assert b'Registration successful!' in response.data
    
    # Verify that the user was created.
    user = User.query.filter_by(email='newuser@example.com').first()
    assert user is not None

def test_register_password_mismatch(client):
    response = client.post('/register', data={
        'email': 'newuser@example.com',
        'password': 'password123',
        'confirm_password': 'differentpassword'
    }, follow_redirects=True)
    
    # Check that the appropriate error message is returned.
    assert b'Passwords do not match' in response.data

# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))