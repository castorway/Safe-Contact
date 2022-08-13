from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from . import models
from . import db

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    return render_template('home.html', user=current_user)

@routes.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html', user=current_user)

