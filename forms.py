from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateField, IntegerField, TimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Register as', 
                      choices=[('donor', 'Blood Donor'), 
                              ('hospital', 'Hospital'), 
                              ('organization', 'Organization')],
                      validators=[DataRequired()])

class DonorProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    blood_type = SelectField('Blood Type', 
                           choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                                   ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
                           validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    address = TextAreaField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(max=50)])
    state = StringField('State', validators=[DataRequired(), Length(max=50)])
    zip_code = StringField('ZIP Code', validators=[DataRequired(), Length(max=10)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    medical_conditions = TextAreaField('Medical Conditions (Optional)')

class HospitalProfileForm(FlaskForm):
    hospital_name = StringField('Hospital Name', validators=[DataRequired(), Length(max=200)])
    license_number = StringField('License Number', validators=[DataRequired(), Length(max=50)])
    contact_person = StringField('Contact Person', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    address = TextAreaField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(max=50)])
    state = StringField('State', validators=[DataRequired(), Length(max=50)])
    zip_code = StringField('ZIP Code', validators=[DataRequired(), Length(max=10)])

class OrganizationProfileForm(FlaskForm):
    organization_name = StringField('Organization Name', validators=[DataRequired(), Length(max=200)])
    registration_number = StringField('Registration Number', validators=[DataRequired(), Length(max=50)])
    contact_person = StringField('Contact Person', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    address = TextAreaField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(max=50)])
    state = StringField('State', validators=[DataRequired(), Length(max=50)])
    zip_code = StringField('ZIP Code', validators=[DataRequired(), Length(max=10)])

class BloodRequestForm(FlaskForm):
    blood_type = SelectField('Blood Type', 
                           choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                                   ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
                           validators=[DataRequired()])
    units_needed = IntegerField('Units Needed', validators=[DataRequired(), NumberRange(min=1, max=20)])
    urgency_level = SelectField('Urgency Level', 
                              choices=[('low', 'Low'), ('medium', 'Medium'), 
                                      ('high', 'High'), ('critical', 'Critical')],
                              validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    needed_by = DateField('Needed By', validators=[DataRequired()])

class DonationEventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    event_date = DateField('Event Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=200)])
    address = TextAreaField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(max=50)])
    state = StringField('State', validators=[DataRequired(), Length(max=50)])
    max_participants = IntegerField('Maximum Participants', validators=[NumberRange(min=1)])

class SearchForm(FlaskForm):
    blood_type = SelectField('Blood Type', 
                           choices=[('', 'All Blood Types'), ('A+', 'A+'), ('A-', 'A-'), 
                                   ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), 
                                   ('O+', 'O+'), ('O-', 'O-')])
    city = StringField('City')
    state = StringField('State')
