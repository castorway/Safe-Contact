from flask import Blueprint, render_template, request, flash, redirect, url_for, session
# Blurprint - helps create routes for different links/paths in a web app
# render_template - renders a html file
# request - allows us to get data from a form
# flash - allows us to display messages to the user (flash a message)

# from .models import User  # get the User schema to update db
from werkzeug.security import generate_password_hash, check_password_hash
# generate_password_hash, used for hashing password in the db for security (convert from plain text to smth else)
# check_password_hash

from . import db

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# current_user is connected with UserMixin

import os
from dotenv import load_dotenv
from twilio.rest import Client
# email verification with twilio, and environment variables to safely store our API keys

# creates a blueprint object of all the routes on the website
auth = Blueprint('auth', __name__)

# set up twilio api keys
load_dotenv()
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID = os.environ.get('VERIFY_SERVICE_SID')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@auth.route('/login', methods=["GET", "POST"])
def login():
    # data = request.form  # get the data from the form, url data, etc.
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # looking for a specific entry in the db and filtering by a certain column
        user = User.query.filter_by(email=email).first()
        if user:
            # if a user was found with the same email check the hashed password if it matches with the entered password
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)  # logging in this user
                return redirect(url_for('routes.home'))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category='error')
        
    return render_template('login.html', user=current_user)
    return render_template('login.html')


@auth.route('/logout')
@login_required  # makes sure the user is logged in to see the logout page
def logout():
    logout_user()  # logs the current user out
    return redirect(url_for("auth.login"))


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        #email = request.form.get('email')
        username = request.form.get('username')
        init_password = request.form.get('init_password')
        confirm_password = request.form.get('confirm_password')
        phone_number = request.form.get('phone_number')

        # find if user email already exists, error
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            flash("Account with this phone number already exists.", category='error')
        elif len(username) < 2:
            flash("Username must be greator than 1 character.", category="error")
        elif init_password != confirm_password:
            flash("Passwords don\'t match", category="error")
        elif len(init_password) < 7:
            flash("Password must be at least 7 characters", category="error")

        else:
            # ready for verification; save params and go to verify page
            user_params = {
                'phone_number' : phone_number,
                'username' : username,
                'password' : generate_password_hash(init_password, method="sha256")
            }

            session['user_params'] = user_params
            return redirect(url_for('auth.verify'))

        # return back to the signup page with any flashed error messages
        return render_template('sign_up.html', user=current_user)

    else:

        return render_template('sign_up.html', user=current_user)


@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'GET':
        # make a new verification
        user_params = session['user_params']

        verification_check = client.verify.v2.services(VERIFY_SERVICE_SID).verification_checks.create(to=user_params['phone_number'])
        session['verification_check'] = verification_check

    else:
        verification_check = client.verify.v2.services(VERIFY_SERVICE_SID).verification_checks.create(to=user_params['phone_number'])
        if verification_check.status == 'approved':
            # only if the user enters the correct code do we add the user
            print("Adding new user with params", user_params)

            new_user = User(**user_params)
            db.session.add(new_user)
            db.session.commit()

            # log in the new user
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("routes.home"))
        else:
            flash("Not yet verified.", category="error")
            return render_template('verify.html', user=current_user)


def send_verification(email):
    """ Send email verification code using Twilio
    """
    verification = client.verify.services(VERIFY_SERVICE_SID).verifications.create(
        to=email,
        channel='email'
    )
    print('made verification:', verification.sid, flush=True)

def check_verification(email, code):
    """ Check email verification code using Twilio
    """
    check = client.verify.services(VERIFY_SERVICE_SID).verification_checks.create(
        to=email, code=code
    )    
    return check.status == 'approved'
