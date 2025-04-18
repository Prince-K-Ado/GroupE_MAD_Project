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

def create_user(email, password='password', is_admin=False):
    user = User(email=email, password=generate_password_hash(password), is_admin=is_admin)
    db.session.add(user)
    db.session.commit()
    return user

def create_post(user_id, **kwargs):
    return Post(
        user_id=user_id,
        content=kwargs.get('content', 'Test admin post'),
        category=kwargs.get('category', 'Disaster Aid'),
        status=kwargs.get('status', 'Pending'),
        goal=kwargs.get('goal', 1000.00)
    )

def test_admin_can_approve_post(client):
    admin = create_user('admin1@mail.com', is_admin=True)
    post = create_post(admin.id)
    db.session.add(post)
    db.session.commit()

    # Log in as admin
    client.post('/login', data={'email': admin.email, 'password': 'password'}, follow_redirects=True)

    # Approve the post
    response = client.post('/admin/review', data={'post_id': post.id, 'action': 'approve'}, follow_redirects=True)
    assert f'Post #{post.id} approved.'.encode() in response.data

    # Check in DB
    updated = Post.query.get(post.id)
    assert updated.status == 'Approved'


def test_admin_can_reject_post(client):
    admin = create_user('admin2@mail.com', is_admin=True)
    post = create_post(admin.id)
    db.session.add(post)
    db.session.commit()

    client.post('/login', data={'email': admin.email, 'password': 'password'}, follow_redirects=True)

    response = client.post('/admin/review', data={'post_id': post.id, 'action': 'reject'}, follow_redirects=True)
    assert f'Post #{post.id} rejected.'.encode() in response.data

    updated = Post.query.get(post.id)
    assert updated.status == 'Rejected'


def test_admin_can_complete_campaign(client):
    admin = create_user('admin3@mail.com', is_admin=True)
    post = create_post(admin.id, status='Approved')
    db.session.add(post)
    db.session.commit()

    client.post('/login', data={'email': admin.email, 'password': 'password'}, follow_redirects=True)

    response = client.post('/admin/review', data={'post_id': post.id, 'action': 'complete'}, follow_redirects=True)
    assert f'Post #{post.id} marked as completed.'.encode() in response.data


    updated = Post.query.get(post.id)
    assert updated.status == 'Completed'

   
def test_non_admin_cannot_access_admin_page(client):
    user = create_user('user@mail.com')
    client.post('/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)

    response = client.get('/admin/review', follow_redirects=True)
    assert b'You do not have permission to access this page.' in response.data
