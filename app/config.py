import os
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir, 'MiniGoFundMe.db') # or 'postgresql://user:password@localhost/your_db_name' or 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploading files
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static' , 'uploads')
    