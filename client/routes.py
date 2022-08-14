from sqlite3 import connect
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy import or_

from .models import User, Connection, Text
from . import models
from . import db
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    users = User.query.all()
    connects = Connection.query.order_by(Connection.end_time.desc())
    text = Text.query.order_by(Text.time_sent.desc()) # connection.texts

    return render_template('home.html', user=current_user, users=users, connects=connects, text=text)

@routes.route('/incoming', methods=['GET', 'POST'])
def incoming():
    """Receive an incoming message from a contact."""

    print('Received incoming message:', request.form['From'], request.form['Body'])
    # print(request.form)
    # print(request.__dict__)
    # print(dir(request))
    
    # parse send number
    send_number = request.form['From']
    send_phone_number = request.form['From'][len(send_number)-10:]
    n = len(send_number) - 10
    send_country_code = request.form['From'][:n]
    print('Parsed number:', send_country_code, send_phone_number)

    # get user who sent message
    sender = User.query.filter(
        User.country_code == send_country_code, 
        User.phone_number == send_phone_number
    ).first()

    if sender == None:
        print("SMS was from unknown number.")
    else:
        # add text to corresponding user + most recent connection sent
        connections = Connection.query.filter(Connection.contact_id==sender.id) \
            .order_by(Connection.last_text.desc())
        most_recent_conn = connections.first()

        if most_recent_conn == None:
            print("SMS sent from user who is not a contact in any connections.")
        else:
            # create the new Text
            print("SMS Text added for user", sender.id, "connection", most_recent_conn.id)
            new_text = Text(
                time_sent=datetime.now(),
                reply_contents=request.form['Body'],
                connection_id=most_recent_conn.id
            )

            most_recent_conn.last_recieved = datetime.now()

            db.session.add(new_text)
            db.session.commit()

    # request response
    resp = MessagingResponse()
    resp.message("Message received.")

    return str(resp)

