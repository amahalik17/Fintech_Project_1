# import dependencies
import os, csv
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
import yfinance as yf
from pattern_dict import patterns
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

    pattern = request.args.get('pattern', None)
    stocks = {}

    # Establish connection and cursor
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Create a list of all symbols in my stock db
    cursor.execute("""SELECT * FROM stock""")
    stock_data = cursor.fetchall()

    # Make a symbols list
    symbols_list = [i[1] for i in cursor.fetchall()]

    # shorten list to speed up debugging process
    #symbols_list = symbols_list[0:100]
    #print(symbols_list)

    #df = pd.DataFrame(symbols_list)

    for symbol in symbols_list:
        stocks[symbol][0] = {"Company": symbol}
        #df = yf.download(symbol, start='2022-01-14', end='2022-02-14')
    print(stocks)
    
    cursor.execute("""SELECT stock_id, date, open, high, low, close FROM stock_price ORDER BY date DESC""")
    price_data = cursor.fetchall()

    #price_df = pd.DataFrame(price_data)

    if pattern:
        for symbol in symbols_list:
            price_df = pd.DataFrame(price_data)
            pattern_func = getattr(talib, pattern)
            try:
                result = pattern_func(price_df[2], price_df[3], price_df[4], price_df[5])
                print(result)
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
    search = request.args.get('search', None)
    # Establish connection and cursor
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # Create a list of all symbols in my stock db
    cursor.execute("""SELECT symbol FROM stock""")
    symbols_list = [i[0] for i in cursor.fetchall()]

    stock_filter = request.args.get('filter', None)
    
    if stock_filter == 'new_closing_high':
        cursor.execute("""
        select * from (
            select symbol, name, stock_id, max(close), date
            from stock_price join stock on stock.id = stock_price.stock_id
            group by stock_id
            order by symbol
        ) where date = ?
        """, (date.today().isoformat(),))
    
    elif stock_filter == 'new_closing_low':
        cursor.execute("""
        select * from (
            select symbol, name, stock_id, min(close), date
            from stock_price join stock on stock.id = stock_price.stock_id
            group by stock_id
            order by symbol
        ) where date = ?
        """, (date.today().isoformat(),))

    # Loop through list of symbols to display searched symbol
    elif search in symbols_list:
        cursor.execute("""SELECT id, symbol, name FROM stock WHERE symbol = ?""",(search,))
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

    cursor.execute("""SELECT id, symbol, name FROM stock WHERE symbol = ?""",(symbol,))
    row = cursor.fetchone()

    cursor.execute("""SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC""", (row['id'],))
    prices = cursor.fetchall()

    return render_template('charts.html', stock=row, symbol=symbol, bars=prices, user=current_user)

