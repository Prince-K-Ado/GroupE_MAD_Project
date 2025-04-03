import random
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
        captcha_response = request.form.get('captcha')

        # Validate the recaptcha response
        if not captcha_response or int(captcha_response) != session.get('captcha_result'):
            flash('Invalid reCAPTCHA response. Please try again.', 'danger')
            # Reload the recaptcha challenge

            a = random.randint(1, 10)
            b = random.randint(1, 10)
            session['captcha_result'] = a + b
            session['captcha_question'] = f"What is {a} + {b} = ?"
            return render_template('register.html', captcha_question=session['captcha_question'])
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html', captcha_question=session['captcha_question'])
        
        if User.query.filter_by(email=email).first():
            flash('User already exists.', 'warning')
            return render_template('register.html', captcha_question=session['captcha_question'])
        
        new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()  # This must be within an active app context
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    else:
        # On get request, generate a new captcha question
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        session['captcha_result'] = a + b    
        session['captcha_question'] = f"What is {a} + {b} = ?"
        return render_template('register.html', captcha_question=session['captcha_question'])    
   
@main.route('/successful_campaigns')
def successful_campaigns():
    if 'user_id' not in session:
        flash('Please log in to view successful campaigns.', 'warning')
        return redirect(url_for('main.login'))
    
    # Get all successful posts, ordered by timestamp
    successful_posts = Post.query.filter_by(is_successful=True).order_by(Post.timestamp.desc()).all()
    return render_template('successful_campaigns.html', posts=successful_posts)

@main.route('/mark_as_successful/<int:post_id>', methods=['POST'])
def mark_as_successful(post_id):
    if 'user_id' not in session:
        flash('Please log in to perform this action.', 'warning')
        return redirect(url_for('main.login'))
    
    post = Post.query.get_or_404(post_id)
    
    # Verify post belongs to current user
    if post.user_id != session['user_id']:
        flash("You can't mark someone else's post as successful.", 'danger')
        return redirect(url_for('main.feed'))
    
    # Toggle the successful status
    post.is_successful = True
    db.session.commit()
    
    flash('Post marked as successful campaign!', 'success')
    return redirect(url_for('main.feed'))

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

@main.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to update your profile.", "warning")
        return redirect(url_for('auth.login'))  # Or however your login route is set up

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('main.profile'))

    # Handle uploaded profile photo
    profile_photo = request.files.get('profile_photo')
    if profile_photo and profile_photo.filename != '':
        filename = secure_filename(profile_photo.filename)
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)  # Make sure the folder exists
        photo_path = os.path.join(upload_folder, filename)
        profile_photo.save(photo_path)
        user.profile_photo_url = url_for('static', filename=f'uploads/{filename}')

    # Update text fields
    user.about_me = request.form.get('about_me', user.about_me).strip() or user.about_me
    user.twitter_handle = request.form.get('twitter_handle', user.twitter_handle).strip() or user.twitter_handle
    user.instagram_handle = request.form.get('instagram_handle', user.instagram_handle).strip() or user.instagram_handle


    # Save changes
    try:
        db.session.commit()
        flash("Profile updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while updating your profile.", "danger")
        print("Update error:", e)

    return redirect(url_for('main.profile'))