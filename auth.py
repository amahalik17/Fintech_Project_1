# import dependencies
import os, csv
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from models import Users, Comments
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
from flask_login import login_user, login_required, logout_user, current_user
import json
import yfinance as yf
from pattern_dict import patterns#, grab_data
import pandas as pd
import talib
import sqlite3
import alpaca_trade_api as tradeapi
from config import alpaca_api_key, alpaca_secret, base_url, db_path
from datetime import date

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
    #grab_data()
    pattern = request.args.get('pattern', None)
    stocks = {}

    with open('otherdata/sp500names.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'Company': row[1]}
    print(stocks)

    if pattern:
        #print(pattern)
        datafiles = os.listdir('Data')
        for filename in datafiles:
            df = pd.read_csv('Data/{}'.format(filename))
            #print(df)
            pattern_func = getattr(talib, pattern)
            symbol = filename.split('.')[0]
            try:
                result = pattern_func(df['Open'], df['High'], df['Low'], df['Close'])
                last = result.tail(1).values[0]
                if last > 0:
                    stocks[symbol][pattern] = "Bullish"
                elif last < 0:
                    stocks[symbol][pattern] = "Bearish"
                else:
                    stocks[symbol][pattern] = None
            except:
                pass
    return render_template('patterns.html', users=current_user, patterns=patterns, stocks=stocks, current_pattern=pattern)



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


@auth.route("/stock_info", methods=['GET', 'POST'])
#@login_required
def stock_info():

    stock_filter = request.args.get('filter', None)

    # Establish connection and cursor
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if stock_filter == 'new_closing_high':
        cursor.execute("""
        select * from (
            select symbol, name, stock_id, max(close), date
            from stock_price join stock on stock.id = stock_price.stock_id
            group by stock_id
            order by symbol
        ) where date = ?
        """, (date.today().isoformat(),))
    else:
        cursor.execute("""SELECT id, symbol, name FROM stock ORDER BY symbol""")
    
    rows = cursor.fetchall()

    return render_template('stock_info.html', stocks=rows, users=current_user)


@auth.route("/charts/<symbol>", methods=['GET', 'POST'])
#@login_required
def charts(symbol):

    # Establish connection and cursor
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM strategy""")
    strategies = cursor.fetchall()

    cursor.execute("""SELECT id, symbol, name FROM stock WHERE symbol = ?""",(symbol,))
    row = cursor.fetchone()

    cursor.execute("""SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC""", (row['id'],))
    prices = cursor.fetchall()

    return render_template('charts.html', stock=row, symbol=symbol, bars=prices, users=current_user, strategies=strategies)



@auth.route("/apply_scanner", methods=['GET', 'POST'])
#@login_required
def apply_scanner():

    if request.method == 'POST':
        stock_id = request.form['stock_id']
        strategy_id = request.form['strategy_id']

        # Establish connection and cursor
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?, ?)
        """, (stock_id, strategy_id))

        connection.commit()

    return redirect(url_for('auth.strategies', strategy_id=strategy_id, stock_id=stock_id))
    #return render_template('strategies.html', users=current_user, strategy_id=strategy_id, stock_id=stock_id)


@auth.route("/strategies/<strategy_id>", methods=['GET', 'POST'])
#@login_required
def strategies(strategy_id):

    # Establish connection and cursor
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name FROM strategy WHERE id = ?
    """, (strategy_id,))
    strategy = cursor.fetchone()

    cursor.execute("""
        SELECT symbol, name
        FROM stock JOIN stock_strategy on stock_strategy.stock_id = stock.id
        WHERE strategy_id = ?
    """, (strategy_id,))

    stocks = cursor.fetchall()

    return render_template('strategies.html', stocks=stocks, users=current_user, strategy=strategy)