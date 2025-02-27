from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

# Create a single SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Bind the SQLAlchemy instance to this app
    db.init_app(app)
    
    # Import models so they are registered with SQLAlchemy
    from app import models

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app
