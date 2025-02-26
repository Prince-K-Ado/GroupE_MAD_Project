from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

# For demonstration, using a simple in-memory user "database"
users = {
    "user@example.com": "password123"
}

# @main.route('/')
# def index():
#     # Redirect to login if not logged in
#     if not session.get('user'):
#         return redirect(url_for('main.login'))
#     return f"Hello, {session.get('user')}! Welcome back."

@main.route('/')
def welcome():
    return render_template('welcome.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        # Simple credential check
        if user and check_password_hash(user.password, password):
            session['user'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('main.feed'))
        elif email in users and users[email] == password:
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('main.feed'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

# @main.route('/logout')
# def logout():
#     session.pop('user', None)
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('User already exists.', 'warning')
            return render_template('register.html')
        # Create a new user with hashed password
        new_user = User(email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')
@main.route('/feed', methods=['GET', 'POST'])
def feed():
    # Require login to access the feed
    if 'user_id' not in session:
        flash('Please log in to access the feed.', 'warning')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        # For demo purposes, handle media file upload (picture or video)
        media = request.files.get('media')
        content = request.form.get('content')
        if media:
            # Add file type, size validations here and store the file as needed.
            filename = media.filename
            flash('Media uploaded successfully!', 'success')
        else:
            filename = None
            flash('No file selected.', 'warning')
        new_post = Post(user_id=session['user_id'], content=content, media=filename)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
    return redirect(url_for('feed.html'))

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))
