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
    profile_photo_url = db.Column(db.String(200))
    about_me = db.Column(db.Text)
    twitter_handle = db.Column(db.String(80))
    instagram_handle = db.Column(db.String(80))
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
    #Timestamp for when the post was created and media was uploaded
    media_filename = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    is_successful = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Post {self.id} by User {self.user_id}>"