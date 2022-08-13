from . import db # import the database from the website package
from flask_login import UserMixin # custom user class to inherit from
from sqlalchemy.sql import func # import the func function from sqlalchemy and gives default values by itself

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(10), unique=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150))
    