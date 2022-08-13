from . import db # import the database from the website package
from flask_login import UserMixin # custom user class to inherit from
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

# Base = declarative_base()

# association_table = Table(
#     "association",
#     Base.metadata,
#     Column("admin_id", ForeignKey("user.id"), primary_key=True),
#     Column("contact_id", ForeignKey("user.id"), primary_key=True),
#     Column("connection_id", ForeignKey("connection.id"), primary_key=True),
# )

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(10), unique=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True)

    # connection_id = Column(db.Integer)
    
class Connection(db.Model):
    __tablename__ = "connection"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    last_text = db.Column(db.DateTime)
    interval = db.Column(db.DateTime)

    # admin_id = db.Column(db.Integer)
    # #admin = db.relationship("User", secondary=association_table, back_populates="connections", foreign_keys="admin_id")

    # contact_id = db.Column(db.Integer)
    #contact = db.relationship("User", secondary=association_table, back_populates="connections", foreign_keys="contact_id")