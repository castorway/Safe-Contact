from . import db # import the database from the website package
from flask_login import UserMixin # custom user class to inherit from
from sqlalchemy import Column, ForeignKey, Integer, Table, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import declarative_base, relationship

user_connection_table = Table('user_connection_table', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('connections_id', db.Integer, db.ForeignKey('connections.id'))
)

class User(db.Model, UserMixin):
    #__tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(10), unique=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True)

    connections = db.relationship("Connections", secondary=user_connection_table, 
        backref='users')

class Connections(db.Model):
    #__tablename__ = "connect"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    last_text = db.Column(db.DateTime)
    interval = db.Column(db.DateTime)

    admin_id = db.Column(db.Integer)
    contact_id = db.Column(db.Integer)