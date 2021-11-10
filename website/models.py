# imoprt db from current directory(db) (init.py db)
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # how to associate notes unique to each user(foreign key)
    # fk(user.id) is referenceing user class(obkect)'s pk which is id as shown below
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    notes = db.relationship('Notes')
