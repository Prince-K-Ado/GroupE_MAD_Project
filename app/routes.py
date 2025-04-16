import random
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app import db
from app.models import User, Post, Subscription, Notification, Category
from sqlalchemy import func
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
            session['is_admin'] = user.is_admin
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
        category = request.form.get('category') # Category of the post (e.g., "Donations", "Food", etc.)
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
        new_post = Post(
            user_id=session['user_id'], 
            content=content, 
            media_filename=filename,
            status='Pending',  # Default status for new posts
            category=category)  # Store the category of the post)
        
        db.session.add(new_post)
        db.session.commit()
        flash("The campaign you have submitted is under review. Please allow 24 hrs for approval.", "info")
        return redirect(url_for('main.profile'))
    # Retrieve all posts from the database
    #posts = Post.query.order_by(Post.timestamp.desc()).all()
    # For Get requests, only show posts that are approved
    approved_posts = Post.query.filter_by(status='Approved').order_by(Post.timestamp.desc()).all()
    return render_template('feed.html', posts=approved_posts)

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
    # Get all posts by the logged-in user
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    return render_template('profile.html', user=user, posts=posts)


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

# Admin page for reviewing posts
# This route is only accessible to admin users
@main.route('/admin/review', methods=['GET', 'POST'])
def admin_review():
    # Check if user is logged in and is an admin.
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('main.login'))
    
    user = User.query.get_or_404(session['user_id'])
    if not user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.feed'))
    
    if request.method == 'POST':
        # Handle post approval/rejection.
        post_id = request.form.get('post_id')
        action = request.form.get('action')  # Expected values: 'approve' or 'reject'
        post = Post.query.get_or_404(post_id)
        
        if action == 'approve':
            post.status = 'Approved'
            flash('Post approved!', 'success')
            
            # Get the Category object matching the post's category (case-insensitive)
            cat_obj = Category.query.filter(func.lower(Category.name) == func.lower(post.category)).first()
            
            # If a matching Category is found, get subscriptions by category_id
            if cat_obj:
                subscriptions = Subscription.query.filter_by(category_id=cat_obj.id).all()
            else:
                subscriptions = []
            
            for subscription in subscriptions:
                # Use a default value if post.category is None (shouldn't be, if enforced)
                category_value = post.category or "General"
                notification = Notification(
                    user_id=subscription.user_id,
                    post_id=post.id,
                    message=f"A new post in category '{category_value}' has been approved."
                )
                db.session.add(notification)
        elif action == 'reject':
            post.status = 'Rejected'
            flash('Post rejected.', 'info')
        
        db.session.commit()
        return redirect(url_for('main.admin_review'))
    
    # For GET, retrieve all pending posts for admin review.
    pending_posts = Post.query.filter_by(status='Pending').order_by(Post.timestamp.desc()).all()
    return render_template('admin_review.html', posts=pending_posts)

@main.route('/notifications')
def notifications():
    if 'user_id' not in session:
        flash('Please log in to see notifications.', 'warning')
        return redirect(url_for('main.login'))
    user_id = session['user_id']
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', notifications=notifications)

@main.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)

@main.route('/notification/read/<int:notif_id>')
def read_notification(notif_id):
    if 'user_id' not in session:
        flash('Please log in to see notifications.', 'warning')
        return redirect(url_for('main.login'))
    notification = Notification.query.get_or_404(notif_id)
    if notification.user_id != session['user_id']:
        flash("You are not allowed to read this notification.", 'danger')
        return redirect(url_for('main.notifications'))
    notification.is_read = True
    db.session.commit()
    return redirect(url_for('main.feed', post_id=notification.post_id))

@main.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if 'user_id' not in session:
        flash('Please log in to manage your preferences.', 'warning')
        return redirect(url_for('main.login'))
    user = User.query.get_or_404(session['user_id'])
    # Retrieve available categories from the database
    available_categories = Category.query.order_by(Category.name).all()
    
    from app.models import Subscription
    if request.method == 'POST':
        # Get list of category names selected by the user
        selected_names = request.form.getlist('categories')
        # Remove all existing subscriptions for the user
        Subscription.query.filter_by(user_id=user.id).delete()
        # Create new subscriptions for each selected category
        for cat_name in selected_names:
            category = Category.query.filter_by(name=cat_name).first()
            if category:
                sub = Subscription(user_id=user.id, category_id=category.id)
                db.session.add(sub)
        db.session.commit()
        flash('Your subscription preferences have been updated.', 'success')
        return redirect(url_for('main.profile'))
    else:
        # For GET, retrieve existing subscriptions as category IDs
        current_subs = Subscription.query.filter_by(user_id=user.id).all()
        current_category_ids = [sub.category_id for sub in current_subs]
        return render_template('preferences.html', available_categories=available_categories, current_category_ids=current_category_ids)
