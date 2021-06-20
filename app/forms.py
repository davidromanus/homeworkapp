from flask_wtf import FlaskForm 
from wtforms import FileField,SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired,Length

class file_upload_form(FlaskForm):
	matric_no=StringField('Matric Number',validators=[DataRequired()])
	submit=SubmitField('Send')

class LoginForm(FlaskForm):
	"""docstring for LoginForm"""
	username=StringField('Enter Username',validators=[DataRequired(),Length(min=8,max=120)])
	password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=120)])
	submit=SubmitField('Login')

class AddStudent(FlaskForm):
	fname=StringField('First Name',validators=[DataRequired()])
	lname=StringField('Last Name',validators=[DataRequired()])
	oname=StringField('Other Name',validators=[DataRequired()])
	matric_no=StringField('Matric Number',validators=[DataRequired()])
	submit=SubmitField('Add Student')

class Edit_student_data(FlaskForm):
	fname=StringField('First Name',validators=[DataRequired()])
	lname=StringField('Last Name',validators=[DataRequired()])
	oname=StringField('Other Name',validators=[DataRequired()])
	matric_no=StringField('Matric Number',validators=[DataRequired()])
	submit=SubmitField('Update')
