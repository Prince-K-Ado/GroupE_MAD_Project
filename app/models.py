from app import app, db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    # __bind_key__ = 'minigofundme'
    # __bind_key__ = 'sqlite'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Flag to indicate if the user is an admin
    # Additional fields can be added here, e.g., name, profile image, etc.
    # A one-to-many relationship can be established with another model, e.g., a user can have many posts

    donations = db.relationship('Donation', back_populates='donor', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)
   
    def __repr__(self):
        return f"<User {self.email}>"
    
class Post(db.Model):
    __tablename__ = 'post'
    # __bind_key__ = 'minigofundme'
    # __bind_key__ = 'sqlite'
    id = db.Column(db.Integer, primary_key=True)
    #Link to the user who created the post
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(140), nullable=False)
    media_filename = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(55), nullable=False) # Category of the post (e.g., "Help Needed", "Donation", etc.)
    status = db.Column(db.String(55), nullable=False, default='Pending') # Status of the post (e.g., "Pending", "Approved", "Rejected")
    timestamp = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow) # Timestamp for when the post was created
    goal = db.Column(db.Numeric(10, 2), nullable=False) # Goal amount for the post
    # New relationship to link to the post
    author = db.relationship('User', backref='posts', lazy=True)
    donations = db.relationship('Donation', back_populates='post', lazy='select', cascade='all, delete-orphan')
    

    def __repr__(self):
        return f"<Post {self.id} by User {self.user_id}>"
    
# Category model to categorize posts
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"
    
# Subscription model to track user subscriptions to posts
class Subscription(db.Model):
    __tablename__ = 'subscription'
    # __bind_key__ = 'minigofundme'
    # __bind_key__ = 'sqlite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # The category the user is subscribed to
    timestamp = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Subscription {self.id} for User {self.user_id} on Post {self.post_id}>"
# drop Subscription table if it exists
# with app.app_context():
#     Subscription.__table__.drop(db.engine)
#     print("Subscription table dropped.")


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # The subscriber
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)    # The post triggering the notification
    message = db.Column(db.String(255), nullable=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Notification {self.id} for user {self.user_id}>"

class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    action = db.Column(db.String(20), nullable=False)  # e.g., "Approved", "Rejected"
    message = db.Column(db.String(255))  # Optional custom message
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AuditLog {self.id} for post {self.post_id}>"

class Donation(db.Model):
    __tablename__ = 'donation'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Use Numeric(10,2) to store currency values accurately.
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    message = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    post = db.relationship('Post', back_populates='donations')
    donor = db.relationship('User', back_populates='donations')

    def __repr__(self):
        return f"<Donation {self.id} by User {self.donor_id} for Post {self.post_id}>"
    

class CampaignUpdate(db.Model):
    __tablename__ = 'campaign_update'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    update_text = db.Column(db.Text, nullable=False)
    media_filename = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<CampaignUpdate {self.id} for Post {self.post_id}>"
