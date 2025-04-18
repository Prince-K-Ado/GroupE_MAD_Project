import pytest
from app import app, db
from app.models import User, Post, Donation
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker
from decimal import Decimal

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

def create_post(user_id, **kwargs):
    post = Post(
        user_id=user_id,
        content=kwargs.get('content', 'Support my cause!'),
        category=kwargs.get('category', 'Health'),
        status=kwargs.get('status', 'Approved'),
        goal=kwargs.get('goal', 500.00)
    )
    db.session.add(post)
    db.session.commit()
    return post

# ----------------- TESTS -----------------

def test_user_can_donate_to_other_campaign(client):
    donor = create_user('donor@mail.com')
    owner = create_user('owner@mail.com')
    post = create_post(owner.id)

    client.post('/login', data={'email': donor.email, 'password': 'password'}, follow_redirects=True)

    response = client.post(f'/donate/{post.id}', data={
        'amount': '25.00',
        'message': 'Hope this helps!'
    }, follow_redirects=True)

    assert b'Thank you for your donation!' in response.data
    donation = Donation.query.filter_by(donor_id=donor.id, post_id=post.id).first()
    assert donation is not None
    assert donation.amount == Decimal('25.00')


def test_user_cannot_donate_to_own_campaign(client):
    user = create_user('selfdonor@mail.com')
    post = create_post(user.id)

    client.post('/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)

    response = client.post(f'/donate/{post.id}', data={
        'amount': '50.00',
        'message': 'This is from me to me.'
    }, follow_redirects=True)

    # We expect the form to still render (not redirect) and show an error
    assert b'You cannot donate to your own campaign' in response.data or b'Invalid donation' in response.data

    # No donation should have been recorded
    donation = Donation.query.filter_by(donor_id=user.id, post_id=post.id).first()
    assert donation is None


def test_invalid_donation_amount_handled(client):
    donor = create_user('donor2@mail.com')
    owner = create_user('owner2@mail.com')
    post = create_post(owner.id)

    client.post('/login', data={'email': donor.email, 'password': 'password'}, follow_redirects=True)

    response = client.post(f'/donate/{post.id}', data={
        'amount': 'invalid!',
        'message': 'Broken amount'
    }, follow_redirects=True)

    assert b'Invalid donation amount' in response.data
    donation = Donation.query.filter_by(donor_id=donor.id, post_id=post.id).first()
    assert donation is None


def test_donations_show_on_my_donations_page(client):
    donor = create_user('donor3@mail.com')
    owner = create_user('owner3@mail.com')
    post = create_post(owner.id)

    # Log in and donate
    client.post('/login', data={'email': donor.email, 'password': 'password'}, follow_redirects=True)
    client.post(f'/donate/{post.id}', data={'amount': '30.00', 'message': 'For your cause!'}, follow_redirects=True)

    # Go to my donations page
    response = client.get('/my_donations', follow_redirects=True)

    assert b'30.00' in response.data or b'$30.00' in response.data
    assert b'For your cause!' in response.data
    assert str.encode(post.content) in response.data
