from flask_login import UserMixin # custom user class to inherit from
from sqlalchemy import Column, ForeignKey, Integer, Table, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import declarative_base, relationship

from . import db # import the database from the website package

class User(db.Model, UserMixin):
    #__tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(10), unique=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True)

class Connection(db.Model):
    __tablename__ = "connection"
    id = db.Column(db.Integer, primary_key=True)

    last_text = db.Column(db.DateTime)
    interval = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    location_tracking = db.Column(db.Boolean)
    text_contents = db.Column(db.String(300))

    admin_id = db.Column(db.Integer)
    contact_id = db.Column(db.Integer)

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_sent = db.Column(db.DateTime)
    reply_contents = db.Column(db.String(300))

    connection_id = db.Column(db.Integer, db.ForeignKey("connection.id"))
    connection = relationship("Connection", backref="texts")