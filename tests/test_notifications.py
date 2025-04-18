import pytest
from app import app, db
from app.models import User, Post, Notification, Category, Subscription
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker


# ----------------- FIXTURE -----------------
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


# ----------------- HELPERS -----------------
def create_user(email, password='password', is_admin=False):
    user = User(email=email, password=generate_password_hash(password), is_admin=is_admin)
    db.session.add(user)
    db.session.commit()
    return user

def create_category(name):
    category = Category.query.filter_by(name=name).first()
    if category:
        return category
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category


def create_post(user_id, category='Health', status='Pending', content='Help me heal'):
    post = Post(
        user_id=user_id,
        content=content,
        category=category,
        status=status,
        goal=1000.00
    )
    db.session.add(post)
    db.session.commit()
    return post

def subscribe_user(user_id, category_name):
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = create_category(category_name)
    subscription = Subscription(user_id=user_id, category_id=category.id)
    db.session.add(subscription)
    db.session.commit()
    

# ----------------- TESTS -----------------

def test_notification_created_on_approval(client):
    # Setup: creator, subscriber, admin
    creator = create_user('creator@example.com')
    subscriber = create_user('subscriber@example.com')
    admin = create_user('admin@example.com', is_admin=True)

    # Subscribe the user to the category
    create_category('Health')
    subscribe_user(subscriber.id, 'Health')

    # Create a post in that category
    post = create_post(creator.id, category='Health')

    # Login as admin and approve the post
    client.post('/login', data={'email': admin.email, 'password': 'password'}, follow_redirects=True)
    client.post('/admin/review', data={'post_id': post.id, 'action': 'approve'}, follow_redirects=True)

    # Check that a notification was created
    notification = Notification.query.filter_by(user_id=subscriber.id, post_id=post.id).first()
    assert notification is not None
    assert notification.message.startswith("A new post in category")


def test_notification_visible_on_login(client):
    user = create_user('user@example.com')
    post = create_post(user.id, category='Health', status='Approved')

    notif = Notification(user_id=user.id, post_id=post.id, message='A test notification')
    db.session.add(notif)
    db.session.commit()

    client.post('/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)
    response = client.get('/notifications', follow_redirects=True)

    assert b'A test notification' in response.data


def test_notification_marked_as_read(client):
    user = create_user('user2@example.com')
    post = create_post(user.id, category='Health', status='Approved')

    notif = Notification(user_id=user.id, post_id=post.id, message='Another notification')
    db.session.add(notif)
    db.session.commit()

    client.post('/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)
    client.get(f'/notification/read/{notif.id}', follow_redirects=True)

    updated = Notification.query.get(notif.id)
    assert updated.is_read is True


def test_no_notification_for_unsubscribed_category(client):
    unsubscribed_user = create_user('unsub@example.com')
    creator = create_user('creator2@example.com')
    admin = create_user('admin2@example.com', is_admin=True)

    create_category('Disaster')
    post = create_post(creator.id, category='Disaster', status='Pending')

    client.post('/login', data={'email': admin.email, 'password': 'password'}, follow_redirects=True)
    client.post('/admin/review', data={'post_id': post.id, 'action': 'approve'}, follow_redirects=True)

    notifications = Notification.query.filter_by(user_id=unsubscribed_user.id).all()
    assert len(notifications) == 0
