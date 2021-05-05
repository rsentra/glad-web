from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm, UpdateForm
from .. import db
from ..models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    add_employee = True
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            glad_id=form.glad_id.data,
                            tel_no=form.tel_no.data,
                            role_id=2 , ##form.role_id.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/edit_register/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_register(id):
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    add_employee = False

    employee = Employee.query.get_or_404(id)  #from table
    print('----update 1----')
    form = UpdateForm(obj=employee) #if not 404
    print('----update 2----')
    if form.validate_on_submit():
        employee.email = email=form.email.data
        employee.username=form.username.data
        employee.glad_id=form.glad_id.data
        employee.tel_no=form.tel_no.data
        employee.role_id=form.role_id.data
        employee.password=form.password.data

        # UPDATE employee to the database
        print('----update----',employee.role_id)
        db.session.commit()
        flash('You have successfully updated! ')

        # # redirect to the login page
        # return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Update')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the appropiate dashboard page after login
            # return redirect(url_for('home.dashboard'))
            if employee.is_admin:
                return redirect(url_for('home.homepage'))
            else:
                return redirect(url_for('home.homepage'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))