import pytest
from app import app, db
from app.models import User, Post
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture(scope='function')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MiniGoFundMe.db'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"connect_args": {"check_same_thread": False}}

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
    transaction.rollback()
    connection.close()

# Helper function
def create_post(user_id, **kwargs):
    """Helper to create a Post with default values and override support."""
    return Post(
        user_id=user_id,
        content=kwargs.get('content', 'Test content'),
        category=kwargs.get('category', 'General Fundraising'),
        status=kwargs.get('status', 'Approved'),
        goal=kwargs.get('goal', 100.00)
    )

def test_view_own_profile_posts(client):
    user = User(email='test_profile@mail.com', password=generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)
    assert b'Login successful!' in response.data

    post = create_post(user.id, content='My profile post')

    db.session.add(post)
    db.session.commit()

    response = client.get('/profile', follow_redirects=True)
    assert b'My profile post' in response.data


def test_profile_redirects_if_not_logged_in(client):
    response = client.get('/profile', follow_redirects=True)
    assert b'Please log in to access your profile.' in response.data


def test_delete_account_removes_user_and_posts(client):
    user = User(email='delete_me@mail.com', password=generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)
    assert b'Login successful!' in response.data

    post = create_post(user.id, content='Delete this post')

    db.session.add(post)
    db.session.commit()

    response = client.post('/delete_account', follow_redirects=True)
    assert b'Your account has been deleted.' in response.data

    assert User.query.filter_by(email='delete_me@mail.com').first() is None
    assert Post.query.filter_by(content='Delete this post').first() is None
