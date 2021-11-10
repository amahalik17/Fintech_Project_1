# import dependencies
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)



@auth.route("/login", methods=['GET', 'POST'])
def login():
    # data = request.form
    # print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # check if user email is valid/in db
        users = Users.query.filter_by(email=email).first()
        if users:
            if check_password_hash(users.password, password):
                flash('Logged in successfully', category='success')
                login_user(users, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', users=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # make sure user doesn't already exist
        users = Users.query.filter_by(email=email).first()
        if users:
            flash('Email already exists.', category='error')

        if len(email) < 7:
            flash('Email must be greater than 6 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            # add user to db
            new_user = Users(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(users, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))


    return render_template('signup.html', users=current_user)


