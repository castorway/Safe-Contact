from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

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
        location_tracking = request.form.get('location_tracking') == 'on'
        text_contents = request.form.get('text_contents')

        admin = User.query.filter_by(username=username).first()
        if admin == None:
            flash(f"User '{username}' not found.")
            return render_template('connection.html', user=current_user)

        # TODO: will need to parse these into datetime
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        interval = request.form.get('interval')

        print("init look", start_time, end_time)

        h, m = [int(x) for x in start_time.split(':')]
        start_time = datetime.now().replace(hour=h, minute=m)

        h, m = [int(x) for x in end_time.split(':')]
        end_time = datetime.now().replace(hour=h, minute=m)

        print(start_time, end_time)

        new_conn = Connection(
            admin_id=admin.id,
            admin_username=admin.username,
            contact_id=current_user.id,
            contact_username=current_user.username,
            interval=int(interval),
            location_tracking=location_tracking,
            text_contents=text_contents,
            start_time=start_time,
            end_time=end_time,
            last_text=datetime.now() - timedelta(minutes=int(interval))
        )

        db.session.add(new_conn)
        db.session.commit()

        return render_template('connection.html', user=current_user)
    else:
        return render_template('connection.html', user=current_user)

@conns.route('/settings', methods=['GET', 'POST'])
# @login_required
def settings():
    if request.method == "POST":
        username = request.form.get('username')
        init_password = request.form.get('init_password')
        confirm_password = request.form.get('confirm_password')
        country_code = request.form.get('country_code')
        phone_number = request.form.get('phone_number')
        print("Settings change submitted for", username, phone_number)

        if username != None:
            current_user.username = username
        
        if (init_password == confirm_password) and (init_password != None):
            current_user.password = generate_password_hash(init_password, method="sha256")
            
        if country_code != None:
            current_user.country_code = country_code
            
        if phone_number != None:
            current_user.phone_number = phone_number

        db.session.commit()

        # return back to the signup page with any flashed error messages
        return render_template('settings.html', user=current_user)

    else:
        return render_template('settings.html', user=current_user)