from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app import db
from app.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

main = Blueprint('main', __name__)

@main.route('/')
def welcome():
    return render_template('welcome.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Query for the user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('main.feed'))
        else:
            print("Login failed for", email)
            flash('Invalid credentials, please try again.', 'danger')
    
    # For GET requests or failed POST attempts, render the login page
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('User already exists.', 'warning')
            return render_template('register.html')
        
        new_user = User(email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()  # This must be within an active app context
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
        # Check if media file was uploaded
        if media and media.filename.strip():
            # Add file type, size validations here and store the file as needed.
            filename = secure_filename(media.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            media.save(upload_path)
            flash('Media uploaded successfully!', 'success')
        else:
            filename = None
            flash('No file selected.', 'warning')
        new_post = Post(user_id=session['user_id'], content=content, media_filename=filename)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('main.feed'))
    # Retrieve all posts from the database
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('feed.html', posts=posts)

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in to access your profile.', 'warning')
        return redirect(url_for('main.login'))
    
    user = User.query.get_or_404(session['user_id'])
    return render_template('profile.html', user=user)


# Delete a post
@main.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    # Ensure the user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to delete posts.', 'warning')
        return redirect(url_for('main.login'))
    
    # Fetch the post; return 404 if not found
    post = Post.query.get_or_404(post_id)
    
    # Only allow deletion if the logged-in user is the owner of the post
    if post.user_id != session['user_id']:
        flash("You cannot delete someone else's post.", 'danger')
        return redirect(url_for('main.feed'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('main.feed'))


# Delete an account
@main.route('/delete_account', methods=['POST'])
def delete_account():
    # Ensure the user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to delete your account.', 'warning')
        return redirect(url_for('main.login'))
    
    user = User.query.get_or_404(session['user_id'])
    
    # Optionally, delete all posts for that user:
    for post in user.posts:
        db.session.delete(post)
    
    db.session.delete(user)
    db.session.commit()
    
    # Log out the user after deletion
    session.pop('user_id', None)
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('main.welcome'))

# Edit a post
@main.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # Ensure the user is logged in
    if 'user_id' not in session:
        flash('Please log in to edit posts.', 'warning')
        return redirect(url_for('main.login'))
    
    post = Post.query.get_or_404(post_id)
    
    # Only allow the owner to edit the post
    if post.user_id != session['user_id']:
        flash("You are not allowed to edit this post.", 'danger')
        return redirect(url_for('main.feed'))
    
    if request.method == 'POST':
        if 'delete' in request.form:
            # User clicked the delete button in the edit form
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully.", "success")
            return redirect(url_for('main.feed'))
        else:
            # Update the post content and optionally update media
            post.content = request.form.get('content')
            media = request.files.get('media')
            if media and media.filename.strip():
                from werkzeug.utils import secure_filename
                filename = secure_filename(media.filename)
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                media.save(upload_path)
                post.media_filename = filename
            db.session.commit()
            flash("Post updated successfully.", "success")
            return redirect(url_for('main.feed'))
    
    # Render the edit form with current post data
    return render_template('edit_post.html', post=post)
