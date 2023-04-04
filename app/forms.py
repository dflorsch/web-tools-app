from datetime import datetime

from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, TextAreaField, \
    SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Optional, Email
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    e_mail = StringField('E-Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Add User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            flash(f'The username {username.data} already exists. Please use a different username!')
            raise ValidationError('Please use a different username.')


class RemoveUserForm(FlaskForm):
    submit = SubmitField('Delete User')


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[Optional()])
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    e_mail = StringField('Email', validators=[Optional(), Email()])
    password = PasswordField('Password', validators=[Optional()])
    submit = SubmitField('Save Changes')


class ProjectForm(FlaskForm):
    agency = StringField('Agency', validators=[DataRequired()])
    customer = StringField('Customer', validators=[DataRequired()])
    project_name = StringField('Project Name', validators=[DataRequired()])
    project_role = StringField('Project Role', validators=[DataRequired()])
    hourly_rate = IntegerField('Hourly Rate', validators=[DataRequired()])
    planned_hours = IntegerField('Planned Hours', validators=[DataRequired()])
    project_start = DateField('Project Start', format='%Y-%m-%d', validators=[DataRequired()])
    project_end = DateField('Project End', format='%Y-%m-%d', validators=[DataRequired()])
    competence_center = StringField('Competence Center', validators=[DataRequired()])
    mentoring_group = StringField('Mentoring Group', validators=[DataRequired()])
    project_extension = BooleanField('Project Extension', validators=[DataRequired()])
    note = TextAreaField('Note', validators=[Optional()])
    submit = SubmitField('Submit')


class ProjectFilterForm(FlaskForm):
    agency = StringField('Agency', validators=[Optional()])
    customer = StringField('Customer', validators=[Optional()])
    competence_center = StringField('Competence Center', validators=[Optional()])
    mentoring_group = StringField('Mentoring Group', validators=[Optional()])
    submit = SubmitField('Filter')


class AttendanceForm(FlaskForm):
    status_choices = [('in_office', 'in_office'), ('sick_leave', 'sick_leave'), ('on_vacation', 'on_vacation')]

    status = SelectField('Status', choices=status_choices, validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    note = TextAreaField('Note', validators=[Optional()])
    submit = SubmitField('Submit')
