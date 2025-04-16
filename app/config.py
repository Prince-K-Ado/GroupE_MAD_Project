import os
from urllib.parse import quote
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
password = quote('12345qwert!@#$%')
# print(f"postgresql://kacatcher:{password}@localhost/minigofundme")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  or 'sqlite:///'+ os.path.join(basedir, 'MiniGoFundMe.db') # or f'postgresql://kacatcher:{password}@127.0.0.1:5432/minigofundme' 
    
    # SQLALCHEMY_BINDS = {
    #     # 'minigofundme': f'postgresql://kacatcher:{password}@127.0.0.1:5432/minigofundme',
    #     'sqlite': 'sqlite:///' + os.path.join(basedir, 'MiniGoFundMe.db')
    # }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


    # Uploading files
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static' , 'uploads')
    

