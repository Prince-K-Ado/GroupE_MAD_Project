# tests/test_login.py
import pytest
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture(scope='function')
def client():
    # Configure app for testing with a persistent file-based SQLite database.
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MiniGoFundMe.db'
    
    # Push an application context
    ctx = app.app_context()
    ctx.push()
    
    # Create tables (if they don't exist)
    db.create_all()
    
    # Begin a connection and start a transaction
    connection = db.engine.connect()
    transaction = connection.begin()
    
    # Create a scoped session using SQLAlchemy's sessionmaker
    SessionFactory = sessionmaker(bind=connection)
    session = scoped_session(SessionFactory)
    db.session = session  # Override the default session with our transactional session
    
    client = app.test_client()
    
    yield client  # Run the test
    
    # Teardown: rollback changes, close session and connection, drop tables, and pop context.
    session.remove()
    transaction.rollback()
    #connection.close()
    #db.drop_all()
    # ctx.pop()

def test_login_success(client):
    # Create a test user
    if not User.query.filter_by(email='test@example.com').first():
        user = User(email='test@example.com', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        
    # Test login with correct credentials
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    # Check that the flash message "Login successful!" is present in the response
    assert b'Login successful!' in response.data

def test_login_failure(client):
    # Create a test user
    if not User.query.filter_by(email='test@example.com').first():
        user = User(email='test@example.com', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        
    # Test login with incorrect password
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    # Check that the flash message for invalid credentials appears
    assert b'Invalid credentials' in response.data

# Drop all tables after tests
with app.app_context():
    db.session.remove()
    #db.drop_all()






# @pytest.fixture(scope='function')
# def client():
#     # Configure the app for testing with a persistent test database.
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MiniGoFundMe.db'
    
#     with app.app_context():
#         db.create_all()
    
#     # Begin a nested transaction
#     connection = db.engine.connect()
#     transaction = connection.begin()
    
#     options = {'bind': connection, 'binds': {}}
#     session = db.create_scoped_session(options=options)
#     db.session = session  # Override the session
    
#     client = app.test_client()
#     yield client
    
#     session.remove()
#     transaction.rollback()
#     connection.close()

# def test_register_success(client):
#     response = client.post('/register', data={
#         'email': 'newuser@example.com',
#         'password': 'password123',
#         'confirm_password': 'password123'
#     }, follow_redirects=True)
    
#     # Check that the registration flash message is in the response
#     assert b'Registration successful!' in response.data
    
#     # Optionally, verify that the user was actually created in the database
#     with app.app_context():
#         user = User.query.filter_by(email='newuser@example.com').first()
#         assert user is not None

# def test_register_password_mismatch(client):
#     response = client.post('/register', data={
#         'email': 'newuser@example.com',
#         'password': 'password123',
#         'confirm_password': 'differentpassword'
#     }, follow_redirects=True)
    
#     # Check that the appropriate error message is returned
#     assert b'Passwords do not match' in response.data





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
