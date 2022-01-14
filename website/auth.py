# import dependencies
import os
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from .models import Users, Comments
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json
import yfinance as yf
from pattern_dict import patterns
import pandas as pd
auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/home')
def home():

    return render_template("home.html", users=current_user)



@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # check if user email is valid/in db
        users = Users.query.filter_by(email=email).first()
        if users:
            if check_password_hash(users.password, password):
                flash('Logged in successfully', category='success')
                login_user(users, remember=True)
                return redirect(url_for('auth.home'))
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
            # login_user(users, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.home'))


    return render_template('signup.html', users=current_user)




@auth.route("/blog", methods=['GET', 'POST'])
@login_required
def blog():
    
    if request.method == 'POST':
        comment = request.form.get('comment')
        
        if len(comment) < 1:
            flash('comment too small', category='error')
        else:
            new_comment = Comments(content=comment, user_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()

            flash('comment added.', category='success')
    
    return render_template('blog.html', users=current_user)



@auth.route('/delete-comment', methods=['POST'])
#@login_required
def delete_comment():
    comment = json.loads(request.data)
    commentId = comment['commentId']
    comment = Comments.query.get(commentId)
    if comment:
        # to make sure user can only delete their own comment
        if comment.user_id == current_user.id:
            db.session.delete(comment)
            db.session.commit()

    return jsonify({})



@auth.route("/patterns", methods=['GET', 'POST'])
#@login_required
def pattern_scanner():
    with open('Data/sp500.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            symbol = company.split(',')[0]
            #print(symbol)
            #df = yf.download(symbol, start='2021-01-14', end='2022-01-14')
            #df.to_csv('./Data/{}.csv'.format(symbol))
    return render_template('patterns.html', users=current_user, patterns=patterns)



@auth.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', users=current_user)


@auth.route("/products", methods=['GET', 'POST'])
def products():
    return render_template('products.html', users=current_user)


@auth.route("/stocks", methods=['GET', 'POST'])
def stocks():
    return render_template('stocks.html', users=current_user)



@auth.route("/options", methods=['GET', 'POST'])
def options():
    return render_template('options.html', users=current_user)



@auth.route("/bonds", methods=['GET', 'POST'])
def bonds():
    return render_template('bonds.html', users=current_user)





