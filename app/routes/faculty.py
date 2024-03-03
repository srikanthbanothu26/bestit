from flask import Blueprint, render_template, redirect, flash, session, request
from app.forms.forms import FacultyForm, FacultyLoginForm
from app.oper.oper import check_faculty_exists, add_faculty
from flask_bcrypt import Bcrypt
from flask_login import login_user
from app.models.models import Faculty

bcrypt = Bcrypt() 
faculty_bp = Blueprint('faculty', __name__)

@faculty_bp.route('/faculty_reg', methods=['GET', 'POST'])
def faculty_reg():
    form = FacultyForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        course = form.course.data
        if not check_faculty_exists(email):
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            add_faculty(email, hashed_password, course)
            flash("Registration successful. Please log in.")
            return redirect('/faculty_login')
        else:
            flash("Username or email already exists. Please choose different credentials.")
    return render_template('faculty_reg.html', form=form)

@faculty_bp.route('/faculty_login', methods=['GET', 'POST'])
def faculty_login():
    form = FacultyLoginForm(request.form)
    print("nothing change")
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        faculty = Faculty.query.filter_by(email=email).first()
        if faculty and bcrypt.check_password_hash(faculty.password_hash, password):
            flash("Login successful.")
            session['email'] = faculty.email
            session['course'] = faculty.course
            user_course = session.get('course')
            return redirect(f"""/{user_course.lower()}_upload""")  
        else:
            flash("Invalid credentials. Login failed.")
    return render_template('faculty_login.html', form=form)


@faculty_bp.route('/python_upload', methods=["GET", "POST"])
def python_upload():
    if 'email' not in session:
        return redirect('/faculty_login')
    
    # Fetch current user's email from the session
    user_email = session['email']

    # Query the database to get the faculty information based on the email
    faculty = Faculty.query.filter_by(email=user_email).first()

    # Check if the faculty information is found
    if faculty:
        # Pass the user information to the HTML template
        return render_template("PYTHON.html", email=faculty.email, id=faculty.id, course=faculty.course)
    else:
        # Handle the case where faculty information is not found
        return "Faculty information not found."


@faculty_bp.route('/java_upload', methods=["GET", "POST"])
def java_upload():
    if 'email' not in session:
        return redirect('/faculty_login')
    return render_template("JAVA.html")
