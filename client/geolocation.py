from sqlite3 import connect
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy import or_

from .models import User, Connection, Text
from . import models
from . import db
from datetime import datetime
import json

geo = Blueprint('geo', __name__)

@geo.route('/ping_location', methods=['GET', 'POST'])
def ping_location():
    if request.method == 'GET':
        # user just visited page
        conn_id = request.query_string[3:]
        print("Location page visited for", conn_id)

        conn = Connection.query.filter(Connection.id == int(conn_id)).first()
        contact_id = conn.contact_id
        print("Contact id:", contact_id)

        return render_template('ping_location.html', first_load=True, contact_id=str(contact_id))
    else:
        # page submitted geolocation data
        data = json.loads(request.data)
        print(data)
        print("Location pinged for contact_id:", data["contact_id"])
        contact_id = data["contact_id"]

        connections = Connection.query.filter(Connection.contact_id == contact_id)
        for connection in connections:
            connection.lat = data["lat"]
            connection.long = data["long"]
            connection.accuracy = data["accuracy"]
        
        db.session.commit()

        return render_template('ping_location.html', first_load=False)
