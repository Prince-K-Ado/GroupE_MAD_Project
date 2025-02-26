from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'your-secret-key' 
    app.config.from_object(Config)

    db.init_app(app) 

    from app.routes import main
    app.register_blueprint(main)

    return app
