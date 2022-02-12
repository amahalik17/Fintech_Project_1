# import dependencies
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from auth import auth
from config import db_path
import sqlite3
from create_db import create_db_tables


app = Flask(__name__)
app.secret_key = "__privatekey__"
#db = SQLAlchemy(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fintech_app.db'
#app.config['SECRET_KEY'] = '12345678910'

def __init__(self):
    connection = sqlite3.connect(db_path)
    #connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS testing(a text, b text, c text)""")
    #rows = cursor.fetchall()
    connection.commit()
    
__init__(app)


#db.init_app(app)

app.register_blueprint(auth, url_prefix='/')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("""SELECT id FROM users""")
    users = cursor.fetchone()
    print(users)
    return users.query.get(int(id))

if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)


