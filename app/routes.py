#imports section
import os
from app import app,db,ALLOWWED_EXTENSIONS,login
from flask import render_template,request,url_for ,redirect,flash,send_file
from werkzeug.utils import secure_filename
from flask import send_from_directory
from app.forms import file_upload_form,LoginForm,AddStudent,Edit_student_data
from app.models import StudentData,FileModel,User
from flask_login import UserMixin,LoginManager,current_user,login_user,logout_user,login_required
from io import BytesIO





#file format checker
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWWED_EXTENSIONS

#file upload routes routes section
@app.route('/',methods=['POST','GET'])
def index():
	form=file_upload_form()
	if form.validate_on_submit():
		check_matric_number=StudentData.query.filter_by(matric_no=form.matric_no.data).first()
		if  check_matric_number:
			return redirect(url_for('upload_file'))
		else:
			flash('You matric number does not exist')
			return redirect(url_for('index'))
	return render_template('index.html',title='Index Page',form=form)


#this function handles file processing and storage into the database
@app.route('/upload_file',methods=['GET','POST'])
def upload_file():
	#form=file_upload_form()
	if request.method=='POST':
		file=request.files['file']
		if file and allowed_file(file.filename):
			filename=secure_filename(file.filename)
			flash('your file has been uploaded successfully','success')
			newfile=FileModel(name=file.filename,data=file.read())
			db.session.add(newfile)
			db.session.commit()
			return redirect(url_for('upload_file',filename=filename))
		else:
			flash('your file type is incorrect. Files must be either txt or pdf. Files larger tham 16m will not be uploaded')
			return redirect(url_for('upload_file'))
	return render_template('upload.html')


#authentication section. The blocks of code below wil handle the user access and permissions i.e
#it checks if a lecturer can login or logout of the network
#only registered users can login the registration must be done only by the admibn of the site
@app.route('/login',methods=['POST','GET'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.get(1)
		login_user(user)
		flash('logged in','success')
		return redirect(url_for('admin_dashboard'))
	return render_template('login.html',title='Login Auth',form=form)
		
	


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))
#the section below contains the admin dashboard route. The admin is super user


@app.route('/superuser_dashboard')
@login_required
def admin_dashboard():
	students=StudentData.query.all()
	return render_template('admin.html',title='Dashboard',students=students)


@app.route('/add_student',methods=['POST','GET'])
@login_required
def add_student():
	form=AddStudent()
	if form.validate_on_submit():
		add=StudentData(fname=form.fname.data,lname=form.lname.data,other_name=form.oname.data,matric_no=form.matric_no.data)
		flash('Student Added Successfully','Success')
		db.session.add(add)
		db.session.commit()
		return redirect(url_for('admin_dashboard'))
	return render_template('add_student.html',title='Add Student Data',form=form)

@app.route('/edit_student_data/<int:id>',methods=['POST','GET'])
@login_required
def edit_student_data(id):
	form=Edit_student_data()
	student_to_edit=StudentData.query.get_or_404(id)

	if request.method=='POST':
		student_to_edit.fname=form.fname.data
		student_to_edit.lname=form.lname.data
		student_to_edit.other_name=form.oname.data
		student_to_edit.matric_no=form.matric_no.data
		db.session.commit()
		flash('Updated Student\'s data Successfully','success')
		return redirect(url_for('admin_dashboard',fname=student_to_edit.fname,lname=student_to_edit.lname,
			other_name=student_to_edit.other_name,matric_no=student_to_edit.matric_no))
	elif request.method=='GET':
		form.fname.data=student_to_edit.fname
		form.lname.data=student_to_edit.lname
		form.oname.data=student_to_edit.other_name
		form.matric_no.data=student_to_edit.matric_no
	return render_template('edit_student_data.html',form=form)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
	item_to_delete=StudentData.query.get_or_404(id)
	db.session.delete(item_to_delete)
	db.session.commit()
	flash('Student Data Removed','success')
	return redirect(url_for('admin_dashboard'))



@app.route('/file_list_page')
@login_required
def file_list_page():
	files=FileModel.query.all()
	return render_template('files.html',title='Uploaded Files Page',files=files)


@app.route('/download/<int:id>')
@login_required
def download(id):
	file_data=FileModel.query.get_or_404(id)
	return send_file(BytesIO(file_data.data),attachment_filename='Assignment_file.pdf',as_attachment=True)