import random
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app import db
from app.models import User, Post, Subscription, Notification, Category, Donation, CampaignUpdate
from decimal import Decimal
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
        gaol_amount = request.form['goal'] # Goal amount for the post
        
        try:
            goal = Decimal(gaol_amount)
        except ValueError:
            flash('Invalid goal amount.', 'Please try again.')
            return redirect(url_for('main.feed'))
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
            category=category,
            goal=goal)  # Store the category of the post)
        
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
# at the top of routes.py, ensure you have:

@main.route('/admin/review', methods=['GET', 'POST'])
def admin_review():
    # --- Security checks ---
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('main.login'))
    admin = User.query.get_or_404(session['user_id'])
    if not admin.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.feed'))

    # --- Handle form submission ---
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        action  = request.form.get('action')  # 'approve', 'reject', or 'complete'
        post    = Post.query.get_or_404(post_id)

        if action == 'approve':
            post.status = 'Approved'
            flash(f'Post #{post.id} approved.', 'success')

        elif action == 'reject':
            post.status = 'Rejected'
            flash(f'Post #{post.id} rejected.', 'info')

        elif action == 'complete':
            post.status = 'Completed'
            flash(f'Post #{post.id} marked as completed.', 'primary')

            # Notify every donor of this campaign ---
            for donation in post.donations:
                # create a friendly summary
                amt = float(donation.amount)
                note = Notification(
                    user_id=donation.donor_id,
                    post_id=post.id,
                    message=(
                        f"Your donation of ${amt:.2f} "
                        f"to the “{post.category}” campaign has been successfully completed."
                    )
                )
                db.session.add(note)

        db.session.commit()
        return redirect(url_for('main.admin_review'))

    # --- Prepare lists for rendering ---
    pending_posts  = Post.query.filter_by(status='Pending') .order_by(Post.timestamp.desc()).all()
    approved_posts = Post.query.filter_by(status='Approved').order_by(Post.timestamp.desc()).all()

    return render_template(
        'admin_review.html',
        pending_posts=pending_posts,
        approved_posts=approved_posts
    )

    

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

    # Calculate the total donations for the post
    total_raised = db.session.query(db.func.coalesce(db.func.sum(Donation.amount), 0)).filter_by(post_id=post_id).scalar()
    donor_count = Donation.query.filter_by(post_id=post_id).count()
    # Get all donations for the post
    donations = Donation.query.filter_by(post_id=post_id).all()
    
    return render_template('view_post.html', post=post, total_raised=total_raised, donor_count=donor_count, donations=donations)



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
    

@main.route('/donate/<int:post_id>', methods=['GET', 'POST'])
def donate(post_id):
    if 'user_id' not in session:
        flash('Please log in to donate.', 'warning')
        return redirect(url_for('main.login'))
    
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        try:
            amount = request.form.get('amount')
            # Convert amount to a Decimal for storing in the database.
            donation_amount = Decimal(amount)
        except Exception as e:
            flash('Invalid donation amount.', 'danger')
            return render_template('donate.html', post=post)
        
        message = request.form.get('message')
        donation = Donation(
            post_id=post.id,
            donor_id=session['user_id'],
            amount=donation_amount,
            message=message
        )

        # Update the post's total amount raised
        note = Notification(
            user_id=post.user_id,
            post_id=post.id,
            message=(
                f"Your campaign “{post.content[:30]}…” "
                f"has received a donation of ${donation_amount:.2f}."
                    )
        )
        db.session.add(note)
        db.session.add(donation)
        db.session.commit()
        flash('Thank you for your donation!', 'success')
        return redirect(url_for('main.view_post', post_id=post.id))
    
    return render_template('donate.html', post=post)

@main.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def post_update(post_id):
    if 'user_id' not in session:
        flash('Please log in to update your campaign.', 'warning')
        return redirect(url_for('main.login'))
    
    post = Post.query.get_or_404(post_id)
    # Ensure the current user is the campaign owner.
    if post.user_id != session['user_id']:
        flash('You are not authorized to update this campaign.', 'danger')
        return redirect(url_for('main.profile'))
    
    if request.method == 'POST':
        update_text = request.form.get('update_text')
        media = request.files.get('media')
        if media and media.filename.strip():
            filename = secure_filename(media.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            media.save(upload_path)
        else:
            filename = None
        
        campaign_update = CampaignUpdate(
            post_id=post.id,
            update_text=update_text,
            media_filename=filename
        )
        db.session.add(campaign_update)
        db.session.commit()
        flash('Your campaign update has been submitted.', 'success')
        return redirect(url_for('main.view_post', post_id=post.id))
    
    return render_template('post_update.html', post=post)


@main.route('/my_donations')
def my_donations():
    if 'user_id' not in session:
        flash('Please log in to see your donations.', 'warning')
        return redirect(url_for('main.login'))
    donations = Donation.query.filter_by(donor_id=session['user_id']) \
                              .order_by(Donation.timestamp.desc()).all()
    return render_template('my_donations.html', donations=donations)
