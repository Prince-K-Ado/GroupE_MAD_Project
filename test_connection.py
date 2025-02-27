from app import app, db

with app.app_context():
    try:
        conn = db.engine.raw_connection()
        print("Successfully created a raw connection!")
        conn.close()
    except Exception as e:
        print("Error while creating raw connection:", e)
