from flask import flash, session, redirect, render_template, Blueprint, current_app,send_from_directory
import os
from app.oper.oper import get_user_course
from flask_wtf.csrf import generate_csrf

course_bp = Blueprint("course", __name__)

@course_bp.route("/python_course", methods=["GET", "POST"])
def python_course():
    csrf_token = generate_csrf()
    if 'username' not in session:
        flash("Please log in first.")
        return redirect('/student_login')
    
    username = session.get('username')
    course = session.get('course')
    
    # Retrieve upload folder paths from the Flask application configuration
    upload_folders = current_app.config.get('UPLOAD_FOLDERS', {}).get('python', {})
    
    # Get the list of files in each upload folder
    file_notes = os.listdir(upload_folders.get('notes', ''))
    file_recordings = os.listdir(upload_folders.get('recordings', ''))
    file_assignments = os.listdir(upload_folders.get('assignments', ''))
    file_assessments = os.listdir(upload_folders.get('assessments', ''))
    
    return render_template("python_course.html", username=username, course=course, 
                           file_notes=file_notes, file_recordings=file_recordings, 
                           file_assignments=file_assignments, file_assessments=file_assessments, csrf_token=csrf_token)

@course_bp.route("/java_course", methods=["GET", "POST"])
def java_course():
    if 'username' not in session:
        flash("Please log in first.")
        return redirect('/student_login')
    
    username = session.get('username')
    course = get_user_course(username)
    
    # Retrieve upload folder paths from the Flask application configuration
    upload_folders = current_app.config.get('UPLOAD_FOLDERS', {}).get('java', {})
    
    # Get the list of files in each upload folder
    file_notes = os.listdir(upload_folders.get('notes', ''))
    file_recordings = os.listdir(upload_folders.get('recordings', ''))
    file_assignments = os.listdir(upload_folders.get('assignments', ''))
    file_assessments = os.listdir(upload_folders.get('assessments', ''))
    
    return render_template("java_course.html", username=username, course=course, 
                           file_notes=file_notes, file_recordings=file_recordings, 
                           file_assignments=file_assignments, file_assessments=file_assessments)

