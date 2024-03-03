#app/forms/form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, Length,DataRequired,ValidationError
import re
from app.models.models import User
from app.models.models import Faculty
from flask_wtf.file import FileField, FileAllowed

class Student_RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    course = SelectField('Select Course', choices=[('python', 'Python'), ('java', 'Java')], validators=[DataRequired()])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already taken")
        
class StudentLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    course = SelectField('Select Course', choices=[('python', 'Python'), ('java', 'Java')], validators=[DataRequired()])

class FacultyForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    course = SelectField('Choose Course', choices=[('python', 'Python'), ('java', 'Java')], validators=[InputRequired()])
    
    def validate_email(self, email):
        email_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"

        if not re.match(email_pattern, email.data):
            raise ValidationError("Invalid email")

        faculty = Faculty.query.filter_by(email=email.data).first()

        if faculty:
            raise ValidationError("Email is already taken")
    
        
class FacultyLoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    course = SelectField('Choose Course', choices=[('python', 'Python'), ('java', 'Java')], validators=[InputRequired()])
    