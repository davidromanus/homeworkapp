import os
from flask import Flask
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 

#configurations secction
ALLOWWED_EXTENSIONS=set(['txt','pdf'])#,'png','jpeg','jpg','gif'
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY']='mysecret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)
login=LoginManager(app)

from app import routes,models,forms