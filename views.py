# import dependencies
import os, csv
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
#import yfinance as yf
from pattern_dict import patterns#, grab_data
import pandas as pd
import talib
import sqlite3
from config import db_path
from datetime import date

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home')
def home():
    return render_template("home.html", user=current_user)


@views.route("/patterns", methods=['GET', 'POST'])
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
    return render_template('patterns.html', user=current_user, patterns=patterns, stocks=stocks, current_pattern=pattern)



@views.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', user=current_user)


@views.route("/products", methods=['GET', 'POST'])
def products():
    return render_template('products.html', user=current_user)


@views.route("/stocks", methods=['GET', 'POST'])
def stocks():
    return render_template('stocks.html', user=current_user)



@views.route("/options", methods=['GET', 'POST'])
def options():
    return render_template('options.html', user=current_user)



@views.route("/bonds", methods=['GET', 'POST'])
def bonds():
    return render_template('bonds.html', user=current_user)


@views.route("/stock_info", methods=['GET', 'POST'])
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

    return render_template('stock_info.html', stocks=rows, user=current_user)


@views.route("/charts/<symbol>", methods=['GET', 'POST'])
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

    return render_template('charts.html', stock=row, symbol=symbol, bars=prices, user=current_user, strategies=strategies)



# @auth.route("/apply_scanner", methods=['GET', 'POST'])
# #@login_required
# def apply_scanner():

#     if request.method == 'POST':
#         stock_id = request.form['stock_id']
#         strategy_id = request.form['strategy_id']

#         # Establish connection and cursor
#         connection = sqlite3.connect(db_path)
#         cursor = connection.cursor()

#         cursor.execute("""
#             INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?, ?)
#         """, (stock_id, strategy_id))

#         connection.commit()

#     return redirect(url_for('auth.strategies', strategy_id=strategy_id, stock_id=stock_id))
#     #return render_template('strategies.html', users=current_user, strategy_id=strategy_id, stock_id=stock_id)


# @auth.route("/strategies/<strategy_id>", methods=['GET', 'POST'])
# #@login_required
# def strategies(strategy_id):

#     # Establish connection and cursor
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     cursor.execute("""
#         SELECT id, name FROM strategy WHERE id = ?
#     """, (strategy_id,))
#     strategy = cursor.fetchone()

#     cursor.execute("""
#         SELECT symbol, name
#         FROM stock JOIN stock_strategy on stock_strategy.stock_id = stock.id
#         WHERE strategy_id = ?
#     """, (strategy_id,))

#     stocks = cursor.fetchall()

#     return render_template('strategies.html', stocks=stocks, users=current_user, strategy=strategy)