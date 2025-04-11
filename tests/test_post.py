import pytest
from app import app, db
from app.models import User, Post
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture(scope='function')
def client():
    # Configure app for testing with a persistent file-based SQLite database.
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MiniGoFundMe.db'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"connect_args": {"check_same_thread": False}}
    
    # Push an application context
    ctx = app.app_context()
    ctx.push()
    
    # Create tables if they don't exist
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
        # db.drop_all()


def login(client, email, password):
    """Helper function to log in."""
    return client.post(
        '/login',
        data={'email': email, 'password': password},
        follow_redirects=True
    )


def test_post_submission_pending(client):
    db.create_all()
    if not User.query.filter_by(email='test@example.com').first():
        user = User(email='test@example.com', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
    # Log in as the test user
    response = login(client, 'test@example.com', 'password')
    assert b'Login successful!' in response.data

    # Submit a new campaign post via the feed route
    post_data = {
        'content': 'This is a test campaign post',
        'category': 'General Fundraising'
        # We're not sending media in this test.
    }
    response = client.post('/feed', data=post_data, follow_redirects=True)

    # The flash message should indicate the post is under review
    assert b'under review' in response.data

    # The user is redirected to the profile page.
    profile_response = client.get('/profile')
    # Check that the post content, category, and a pending-review message appear.
    assert b'This is a test campaign post' in profile_response.data
    assert b'General Fundraising' in profile_response.data
    assert b'under review' in profile_response.data


def test_feed_shows_only_approved(client):
    # Log in as the test user
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


    # Access the feed route, which should show only approved posts.
    # Our test post will be under review (pending), so none should be shown.
    feed_response = client.get('/feed', follow_redirects=True)
    # We expect a "No posts available" message since pending posts aren’t public.
    assert b'No posts available' in feed_response.data

# Drop all tables after tests
with app.app_context():
    db.session.remove()
    #db.drop_all()