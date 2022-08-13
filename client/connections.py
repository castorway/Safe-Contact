from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from .models import User, Connection
from . import models
from . import db

conns = Blueprint('conns', __name__)

@conns.route('/connection', methods=['GET', 'POST'])
# @login_required
def connection():
    if request.method == 'POST':
        # creating a new connection as the contact
        username = request.form.get('username')
        interval = request.form.get('interval')
        location_tracking = request.form.get('location_tracking')
        text_contents = request.form.get('text_contents')
        #emergency_numbers = request.form.get('emergency_numbers')

        admin = User.query.filter_by(username=username).first()

        new_conn = Connection({
            'admin': admin,
            'contact': current_user,
            'interval': interval,
            'location_tracking': location_tracking,
            'text_contents': text_contents
            #'emergency_numbers': emergency_numbers
        })

        db.session.add(new_conn)
        # add conn to list of conns for admin and contact

        return render_template('connection.html', user=current_user)
    else:
        return render_template('connection.html', user=current_user)

