from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    # Additional fields can be added here, e.g., name, profile image, etc.
    # A one-to-many relationship can be established with another model, e.g., a user can have many posts
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
   
    def __repr__(self):
        return f"<User {self.email}>"
    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    #Link to the user who created the post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(140), nullable=False)
    #Timestamp for when the post was created and media was uploaded
    media_filename = db.Column(db.String(255), nullable=True)
    timestampg = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post {self.id} by user {self.user_id}>"
