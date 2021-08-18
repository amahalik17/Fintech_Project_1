# Import flask and dependencies
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.secret_key = "hello"
# app.permanent_session_lifetime = timedelta(days=7) # can do minutes too

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class users(db.Model):
#     _id = db.Column("id", db.Integer, primary_key = True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100))

#     def __init__(self, name, email):
#         self.name = name
#         self.email = email



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/index.html")
def home_page():
    return render_template('index.html')


@app.route("/dataframe.html")
def dataframe():
    #df = pd.read_csv('Data/stock_winners.csv')
    #print(df)
    return render_template('dataframe.html')





if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)


