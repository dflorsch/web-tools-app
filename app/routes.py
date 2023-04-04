from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from datetime import date, timedelta

from app import app, db
from app.email import send_credentials_email
from app.forms import LoginForm, ProjectForm, RemoveUserForm, AddUserForm, ProjectFilterForm, ProfileForm, \
    AttendanceForm
from app.models import User, Project, Attendance


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('welcome.html', title='Welcome')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin')
@login_required
def admin():
    form = LoginForm()
    if not current_user.is_admin:
        flash('You are not authorized to view this page.')
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('admin.html', title='Admin', users=users, form=form)


@app.route('/admin/users')
@login_required
def show_users():
    form = LoginForm()
    if not current_user.is_admin:
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('show_users.html', title='Users', users=users, form=form)


@app.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    e_mail=form.e_mail.data,
                    is_admin=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # send_credentials_email(user, user_pw=form.password.data)
        # smtplib.SMTPAuthenticationError: (535, b'5.7.139 Authentication unsuccessful, SmtpClientAuthentication is
        # disabled for the Tenant. Visit https://aka.ms/smtp_auth_disabled for more information.
        # [FR0P281CA0143.DEUP281.PROD.OUTLOOK.COM 2023-03-31T22:26:09.545Z 08DB319835AA1D8C]')

        flash('New user has been added!')
        return redirect(url_for('show_users'))
    return render_template('add_user.html', title='Add User', form=form)


@app.route('/admin/users/remove/<int:user_id>', methods=['POST'])
@login_required
def remove_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    user = User.query.get_or_404(user_id)
    form = RemoveUserForm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        flash('User has been removed!')
        return redirect(url_for('show_users'))
    return redirect(url_for('show_users'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        if form.password.data:
            current_user.set_password(form.password.data)
        form.populate_obj(current_user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('home'))
    return render_template('profile.html', title='Profile', form=form)


# def create_admin_user():
#     admin_username = "admin"
#     admin_password = "u@HJz1n4fGxUsTwwW*uKAFm3"
#     admin_user = User.query.filter_by(username=admin_username).first()
#
#     if admin_user is None:
#         hashed_password = generate_password_hash(admin_password)
#         admin_user = User(username=admin_username, password_hash=hashed_password, is_admin=True)
#         db.session.add(admin_user)
#         db.session.commit()
#         print(f"Admin user '{admin_username}' has been created.")
#
#
# create_admin_user()


@app.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():
    form = ProjectFilterForm()
    projects_query = Project.query.order_by(Project.project_start.asc()).all()

    if request.method == 'POST':
        agency = request.form['agency']
        customer = request.form['customer']
        competence_center = request.form['competence_center']
        mentoring_group = request.form['mentoring_group']

        # Query the database for projects that match the filter criteria
        projects_query = Project.query.filter(Project.agency.like(f'%{agency}%'),
                                              Project.customer.like(f'%{customer}%'),
                                              Project.competence_center.like(f'%{competence_center}%'),
                                              Project.mentoring_group.like(f'%{mentoring_group}%')).order_by(
            Project.project_start.asc()).all()

    return render_template('projects.html', title='Projects', form=form, projects=projects_query)


@app.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            agency=form.agency.data,
            customer=form.customer.data,
            project_name=form.project_name.data,
            project_role=form.project_role.data,
            hourly_rate=form.hourly_rate.data,
            planned_hours=form.planned_hours.data,
            project_start=form.project_start.data,
            project_end=form.project_end.data,
            competence_center=form.competence_center.data,
            mentoring_group=form.mentoring_group.data,
            project_extension=form.project_extension.data,
            note=form.note.data
        )
        db.session.add(project)
        db.session.commit()
        flash(f'The project has been added. {form.project_extension.data}')
        return redirect(url_for('display_projects'))
    return render_template('add_project.html', title='Add Project', form=form)


@app.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.commit()
        flash('Project has been updated successfully.')
        return redirect(url_for('display_projects'))
    return render_template('edit_project.html', title='Edit Project', form=form, project_id=project_id, project=project)


@app.route('/projects/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    # convert the project_id parameter to an integer
    project_id = int(project_id)

    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project has been deleted successfully.')
    return redirect(url_for('display_projects'))


@app.route('/attendance')
@login_required
def attendance():
    # Get attendance entries based on filters
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if status and status != 'all':
        attendances = Attendance.query.filter_by(status=status)
    else:
        attendances = Attendance.query.all()

    if request.args.get('today'):
        today = date.today()
        start_date = today.strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
        attendances = Attendance.query.filter(
            (Attendance.start_date == start_date) & (Attendance.end_date == end_date) & (Attendance.status == status) |
            ((Attendance.start_date <= start_date) & (Attendance.end_date >= end_date) & (Attendance.status == status)))

    elif request.args.get('this_week'):
        today = date.today()
        start_date = today - timedelta(days=today.weekday())
        end_date = today + timedelta(days=6 - today.weekday())
        attendances = Attendance.query.filter(
            (Attendance.start_date.between(start_date, end_date)) & (Attendance.status == status) |
            ((Attendance.start_date <= start_date) & (Attendance.end_date >= end_date) & (Attendance.status == status)))

    elif start_date and end_date:
        attendances = Attendance.query.filter(
            (Attendance.start_date.between(start_date, end_date)) |
            ((Attendance.start_date <= start_date) & (Attendance.end_date >= end_date)))

    in_office = [a for a in attendances if a.status == 'in_office']
    sick_leave = [a for a in attendances if a.status == 'sick_leave']
    on_vacation = [a for a in attendances if a.status == 'on_vacation']

    return render_template('attendance.html', title='Attendance', in_office=in_office,
                           sick_leave=sick_leave, on_vacation=on_vacation)


@app.route('/add_attendance', methods=['GET', 'POST'])
@login_required
def add_attendance():
    form = AttendanceForm()
    if form.validate_on_submit():
        new_attendance = Attendance(
            user_id=current_user.id,
            status=form.status.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            note=form.note.data
        )
        db.session.add(new_attendance)
        db.session.commit()
        flash('The attendance has been added.')
        return redirect(url_for('attendance'))
    return render_template('add_attendance.html', title='Add Attendance', form=form)
