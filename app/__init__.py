from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
# Create one instance of SQLAlchemy


    
app = Flask(__name__)
app.config.from_object(Config)
# Bind SQLAlchemy to this app
db = SQLAlchemy(app)

# db.init_app(app)
# Import models to register them with SQLAlchemy
from app import models

# Register your blueprints
from app.routes import main as main_blueprint
app.register_blueprint(main_blueprint)


