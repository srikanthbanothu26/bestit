from flask import Blueprint, render_template, redirect, flash, request, session
from app.forms.forms import AssessmentForm
from app.models.models import Assessment, Faculty
from app.extensions.db import db

assessment_bp = Blueprint('assessment', __name__)

@assessment_bp.route('/upload_assessment', methods=['GET', 'POST'])
def upload_assessment():
    form = AssessmentForm()

    if request.method == 'POST':
        if form.validate_on_submit():  # Validate the form
            email = session.get('email')  # Retrieve email from the session
            print(email)
            faculty = Faculty.query.filter_by(email=email).first()
            print(faculty)

            if faculty:
                faculty_id = faculty.id
                course = faculty.course

                # Create a new assessment instance and add it to the database
                assessment = Assessment(
                    question=form.question.data,
                    option1=form.option1.data,
                    option2=form.option2.data,
                    option3=form.option3.data,
                    option4=form.option4.data,
                    correct_answer=form.correct_answer.data,
                    faculty_id=faculty_id,
                    course=course  # Associate the assessment with faculty's course
                )
                db.session.add(assessment)
                db.session.commit()

                flash('Assessment uploaded successfully!', 'success')
                return redirect(f"""/{course.lower()}_upload""")
            else:
                flash('Faculty not found in the database!', 'error')

    return render_template('upload_assessment.html', form=form)


@assessment_bp.route('/assessments/<course>')
def display_assessments(course):
    # Query assessments based on the course
    assessments = Assessment.query.filter_by(course=course).all()
    # Pass the assessments and their indices to the template, along with the enumerate function
    return render_template('displayassessments.html', assessments=assessments, index_start=1, enumerate=enumerate)
