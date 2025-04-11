from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    # __bind_key__ = 'minigofundme'
    # __bind_key__ = 'sqlite'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    # Additional fields can be added here, e.g., name, profile image, etc.
    # A one-to-many relationship can be established with another model, e.g., a user can have many posts
    posts = db.relationship('Post', backref='author', lazy=True)
    
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
    # Timestamp for when the post was created
    timestamp = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post {self.id} by User {self.user_id}>"
    
# Subscription model to track user subscriptions to posts
class Subscription(db.Model):
    __tablename__ = 'subscription'
    # __bind_key__ = 'minigofundme'
    # __bind_key__ = 'sqlite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    category = db.Column(db.String(55), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)

