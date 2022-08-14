from sqlite3 import connect
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy import or_

from .models import User, Connection, Text
from . import models
from . import db
from datetime import datetime

geo = Blueprint('geo', __name__)

@geo.route('/ping_location', methods=['GET', 'POST'])
@login_required
def ping_location():
    if request.method == 'GET':
        # user just visited page
        print("Location page visited for", current_user.id)
        return render_template('ping_location.html')
    else:
        # page submitted geolocation data
        print("Location pinged for", current_user.id)
        print(request.data)

        connections = Connection.query.filter(Connection.contact_id == current_user.id)
        for connection in connections:
            connection.lat = request.data["lat"]
            connection.long = request.data["long"]
            connection.accuracy = request.data["accuracy"]
        
        db.session.commit()

        return render_template('contact_map.html')
