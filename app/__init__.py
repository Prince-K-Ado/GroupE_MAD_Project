from flask import Flask, session
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_mail import Mail



#load_dotenv()
# Create one instance of SQLAlchemy


    
app = Flask(__name__)
app.config.from_object(Config)
# Bind SQLAlchemy to this app
db = SQLAlchemy(app)
mail = Mail(app)

# db.init_app(app)
# Import models to register them with SQLAlchemy
from app import models, routes

# Register your blueprints
from app.routes import main as main_blueprint
app.register_blueprint(main_blueprint)


@app.context_processor
def inject_notification_count():
    from app.models import Notification  # avoid circular import issues if needed
    if 'user_id' in session:
        count = Notification.query.filter_by(user_id=session['user_id'], is_read=False).count()
    else:
        count = 0
    # Print the count to the console for debugging
    print(f"Notification count: {count}")
    return dict(notification_count=count)



