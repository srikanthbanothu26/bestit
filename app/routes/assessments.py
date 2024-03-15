from flask import Blueprint, render_template, redirect, flash, request, session,jsonify
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




@assessment_bp.route('/uploaded_questions/<int:faculty_id>', methods=['GET'])
def get_uploaded_questions(faculty_id):
    faculty = Faculty.query.get(faculty_id)
    if not faculty:
        return jsonify({'error': 'Faculty not found'}), 404

    # Query the Assessment table to fetch questions based on faculty_id
    uploaded_questions = Assessment.query.filter_by(faculty_id=faculty_id).all()
    # Convert the list of Assessment objects to a list of dictionaries
    questions = []
    for question in uploaded_questions:
        questions.append({
            'id': question.id,  # assuming each question has an ID
            'question': question.question,
            'option1': question.option1,
            'option2': question.option2,
            'option3': question.option3,
            'option4': question.option4,
            'correct_answer': question.correct_answer
        })
    print(questions)
    return jsonify(questions)


@assessment_bp.route('/delete_question', methods=['POST'])
def delete_question():
    question_id = request.json.get('question_id')

    # Query the Assessment table by question_id
    question = Assessment.query.get(question_id)

    if question:
        # Delete the question record from the database
        db.session.delete(question)
        db.session.commit()
        return '', 204
    else:
        # Question record not found in the database
        return jsonify({'error': 'Question record not found in the database'}), 404
