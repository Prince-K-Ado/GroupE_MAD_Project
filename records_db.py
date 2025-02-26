import sqlite3
from GroupE.app import create_app, db

app = create_app()

connection = sqlite3.connect('mini_gofundme.db')

with app.app_context() as f:
    db.create_all()
    connection.executescript(f.read())
    print("Database tables created successfully!")





    