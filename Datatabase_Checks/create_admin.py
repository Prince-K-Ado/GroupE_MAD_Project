# create_admin.py
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

admin_email = "testadmin@mail.com"
admin_password = "admin"  # Change this to a secure password

with app.app_context():
    # Check if an admin with the specified email already exists.
    existing_admin = User.query.filter_by(email=admin_email).first()
    if existing_admin:
        print("Admin user already exists.")
    else:
        admin = User(
            email=admin_email,
            password=generate_password_hash(admin_password, method='pbkdf2:sha256'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
