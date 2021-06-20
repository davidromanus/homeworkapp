from app import app,db,login
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
	return User.query.get(user_id)


class User(db.Model,UserMixin):
	"""docstring for Admin"""
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(50),unique=True)
	pw_hash=db.Column(db.String(128))


#the files storage model below:
class FileModel(db.Model):
	"""docstring for File"""
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(200))
	data=db.Column(db.LargeBinary)

#students matric number
class StudentData(db.Model):
	"""docstring for Matric Number"""
	id=db.Column(db.Integer,primary_key=True)
	fname=db.Column(db.String(100))
	lname=db.Column(db.String(120))
	other_name=db.Column(db.String(100))
	matric_no=db.Column(db.String(30),unique=True)
		