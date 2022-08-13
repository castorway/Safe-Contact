from sqlite3 import connect
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from twilio.twiml.messaging_response import MessagingResponse

from .models import User, Connection
from . import models
from . import db

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    users = User.query.all()
    connects = Connection.query.all()

    return render_template('home.html', user=current_user, users=users, connects=connects)

@routes.route('/incoming', methods=['GET', 'POST'])
def incoming():
    """Receive an incoming message from a contact."""

    print(request)

    # request response
    resp = MessagingResponse()
    resp.message("Message received.")

    return str(resp)

