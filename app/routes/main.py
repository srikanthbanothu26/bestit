from flask import Blueprint, render_template, session, redirect, request, flash
from flask_login import login_required

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
    return render_template("pics.html")

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



@main_bp.route("/admin")
def admin():
    return render_template("admin.html")