# import dependencies
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from config import db_pw


db = SQLAlchemy()
db_name = 'my_database'

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '12345678910'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{db_pw}@localhost/{db_name}'
    db.init_app(app)

    from auth import auth

    app.register_blueprint(auth, url_prefix='/')

    from models import Users, Comments

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('Fintech_Project_1' + db_name):
        #db.create_all(app=app)
        print('Created database!')
