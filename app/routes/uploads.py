from flask import flash, redirect, request, session, Blueprint, send_from_directory, jsonify,current_app
from werkzeug.utils import secure_filename
import os
from app import Config
from app.models.models import Faculty, File
from app.extensions.db import db
from datetime import datetime
import pytz

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

uploads_bp = Blueprint('uploads', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@uploads_bp.route('/uploads/<filename>', methods=["GET", "POST"])
def uploaded_file(filename):
    upload_folders = [Config.UPLOAD_FOLDERS[course][file_type] for course in Config.UPLOAD_FOLDERS for file_type in Config.UPLOAD_FOLDERS[course]]
    return ",\n".join(send_from_directory(folder, filename) for folder in upload_folders)


@uploads_bp.route('/upload/<file_type>', methods=["POST"])
def upload_file(file_type):
    if 'email' not in session:
        flash('You must be logged in to upload files', 'error')
        return redirect('/faculty_login')
    
    user_email = session['email']
    faculty_course = session.get('course')
    if faculty_course not in Config.UPLOAD_FOLDERS:
        flash('Invalid course selected', 'error')
        return redirect('/faculty_reg')
    
    if file_type not in Config.UPLOAD_FOLDERS[faculty_course]:
        flash('Invalid file type selected', 'error')
        return redirect('/faculty_home')
    
    upload_folder = Config.UPLOAD_FOLDERS[faculty_course][file_type]
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    files = request.files.getlist('file')
    faculty = Faculty.query.filter_by(email=user_email).first()
    if not faculty:
        flash('Faculty not found', 'error')
        return redirect('/faculty_login')
    
    faculty_id = faculty.id
    
    for file in files:
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            ist_timezone = pytz.timezone('Asia/Kolkata')
            current_time_utc = datetime.utcnow()
            current_time_ist = current_time_utc.astimezone(ist_timezone)
            formatted_date = current_time_ist.strftime('%a, %d %b %Y %H:%M:%S GMT')
            new_file = File(filename=filename, filepath=file_path,faculty_id=faculty_id,day=formatted_date)
            db.session.add(new_file)
            db.session.commit()
                    
            flash('File uploaded successfully', 'success')
        else:
            flash('Invalid file format', 'error')
    
    return redirect(request.referrer + '#success-message')


@uploads_bp.route('/search_files', methods=['POST'])
def search_files():
    search_filename = request.form.get("search_filename")

    if search_filename:
        # Search files by filename
        files = File.query.filter(File.filename.like(f'%{search_filename}%')).all()

    else:
        # No search criteria provided
        files = []

    # Convert file objects to JSON
    files_data = [{'filename': file.filename, 'day': file.day} for file in files]
    return jsonify(files_data)


@uploads_bp.route('/uploaded_files', methods=['GET'])
def get_uploaded_files():
    if 'email' not in session:
        return jsonify([])

    user_email = session['email']
    faculty = Faculty.query.filter_by(email=user_email).first()
    if not faculty:
        return jsonify([])

    user_files = File.query.filter_by(faculty_id=faculty.id).all()
    files = [{'filename': file.filename, 'day': file.day} for file in user_files]
    return jsonify(files)


@uploads_bp.route('/deletefile', methods=['POST'])
def delete_files():
    filename = request.json.get('filename')
    day = request.json.get('day')
    print(filename)
    print(day)

    # Query the file by filename and day
    file = File.query.filter_by(filename=filename, day=day).first()

    if file:
        # Remove the file from the filesystem
        if os.path.exists(file.filepath):
            os.remove(file.filepath)
            print(f"File '{filename}' removed from filesystem.")

        # Delete the file record from the database
        db.session.delete(file)
        db.session.commit()
        print(f"File record '{filename}' deleted from the database.")

        return '', 204
    else:
        # File record not found in the database
        return jsonify({'error': 'File record not found in the database'}), 404
