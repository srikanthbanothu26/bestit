from flask import Blueprint, render_template, session, redirect, request, flash,jsonify,current_app
from flask_login import login_required
from app.models.models import placement,Image
from app.extensions.db import db
from werkzeug.utils import secure_filename
import os


main_bp = Blueprint("main", __name__)

@main_bp.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

@main_bp.route('/main', methods=["GET", "POST"])
@login_required
def main():
    if request.method == "POST":
        user_course = session.get('course')
        if user_course:
            return redirect(f"/{user_course.lower()}_course") 
        else:
            flash("No course selected for the user.")
            return redirect('/student_registration') 
    
    user_course = session.get('course')
    return render_template("main.html", user_course=user_course)

@main_bp.route('/pics', methods=["GET", "POST"])
def pics():
    if request.method == "POST":
        return redirect("/")
    uploaded_images = Image.query.all()
    return render_template("pics.html",uploaded_images=uploaded_images)


UPLOADS_FOLDER = 'uploadingpics'  # Relative path within the static folder

@main_bp.route('/addpics', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.static_folder, UPLOADS_FOLDER)
            filepath = os.path.join(upload_folder, filename)
            print(filepath)

            # Create the upload directory if it doesn't exist
            os.makedirs(upload_folder, exist_ok=True)

            file.save(filepath)

            new_image = Image(filename=filename, filepath=filepath)
            db.session.add(new_image)
            db.session.commit()
            flash('File uploaded successfully')
            return redirect("/admin")

    return render_template("addpics.html")

@main_bp.route('/faculty_home', methods=['GET', 'POST'])
def faculty_home():
    return render_template("faculty_home.html")

@main_bp.route('/python_info', methods=['GET','POST'])
def python_info():
    return render_template('pythoninfo.html')

@main_bp.route('/java_info', methods=['GET','POST'])
def java_info():
    return render_template('javainfo.html')

@main_bp.route('/digitalmarketing_info', methods=['GET','POST'])
def dm_info():
    return render_template('dminfo.html')

@main_bp.route('/testingtools_info', methods=['GET','POST'])
def tt_info():
    return render_template('ttinfo.html')



@main_bp.route("/admin",methods=['get','post'])
def admin():

        # Fetch the placement object from the database
    new_placement = placement.query.all()
    
    return render_template('admin.html', new_placement=new_placement)

from flask import send_from_directory


@main_bp.route('/upload/<filename>')
def uploaded_files(filename):
    print("Filename:", filename)  # Print filename for debugging
    return send_from_directory(UPLOADS_FOLDER, filename)


@main_bp.route('/deleteimages', methods=['GET', 'POST'])
def deleteimages():
    if request.method == 'POST':
        # Check if any images were selected for deletion
        images_to_delete = request.form.getlist('image_checkbox')
        if images_to_delete:
            for image_id in images_to_delete:
                # Retrieve the Image object from the database and delete it
                image = Image.query.get(image_id)
                if image:
                    print(image.filepath)
                    # Delete the image file from the filesystem
                    os.remove(image.filepath)
                    # Delete the image from the database
                    db.session.delete(image)
                    db.session.commit()
            flash('Selected images deleted successfully')
        else:
            flash('No images selected for deletion')

    # Fetch the list of uploaded images from the database
    uploaded_images = Image.query.all()
    for x in uploaded_images:
        print(x)
    return render_template('deletepics.html', uploaded_images=uploaded_images)


@main_bp.route('/delete_placement/<int:placement_id>', methods=['GET','POST'])
def delete_placement(placement_id):
    placement_to_delete = placement.query.get(placement_id)

    if placement_to_delete:
        db.session.delete(placement_to_delete)
        db.session.commit()
        return redirect('/admin') # Redirect to the admin page after deletion
    else:
        return jsonify({"error": "Placement not found"}), 404
