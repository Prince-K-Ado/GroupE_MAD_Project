import sqlite3
from app import create_app, db

app = create_app()

connection = sqlite3.connect('mini_gofundme.db')

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")





    