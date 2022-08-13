from sqlite3 import connect
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user

from .models import User, Connection, user_connection_table
from . import models
from . import db

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    users = User.query.all()
    connects = Connection.query.all()

    return render_template('home.html', user=current_user, users=users, connects=connects)

@routes.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html', user=current_user)

