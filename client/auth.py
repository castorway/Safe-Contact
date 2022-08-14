from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from .models import User  # get the User schema to update db
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

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
        username = request.form.get("username")
        password = request.form.get("password")
        
        # looking for a specific entry in the db and filtering by a certain column
        user = User.query.filter_by(username=username).first()
        if user:
            # if a user was found with the same email check the hashed password if it matches with the entered password
            if check_password_hash(user.password, password):
                #flash("Logged in successfully!", category='success')
                login_user(user, remember=True)  # logging in this user
                return redirect(url_for('routes.home'))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Username or passowrd does not match.", category='error')
        
    return render_template('login.html', user=current_user)

@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get('username')
        init_password = request.form.get('init_password')
        confirm_password = request.form.get('confirm_password')
        country_code = request.form.get('country_code')
        phone_number = request.form.get('phone_number')
        print("Signup submitted for", username, phone_number)

        # find if user email already exists, error
        user = User.query.filter_by(country_code=country_code, phone_number=phone_number).first()
        if user:
            flash("Account with this phone number already exists.", category='error')
        elif len(username) < 2:
            flash("Username must be longer than 1 character.", category="error")
        elif init_password != confirm_password:
            flash("Passwords don\'t match", category="error")
        elif len(init_password) < 7:
            flash("Password must be at least 7 characters", category="error")

        else:
            # ready for verification; save params and go to verify page
            print("Ready to verify user")
            user_params = {
                'phone_number' : phone_number,
                'country_code' : country_code,
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
    print(client.verify.v2.services(VERIFY_SERVICE_SID))
    if request.method == 'GET':
        # first time page loaded; make a new verification
        user_params = session['user_params']
        number = user_params['country_code'] + user_params['phone_number']
        verification_check = client.verify.v2.services(VERIFY_SERVICE_SID).verifications.create(to=number, channel='sms')

        return render_template('verify.html', user=current_user) 

    else:
        # form submitted with code; check verification
        print(request.form)
        code = [request.form[f'num-{i}'] for i in range(1, 7)]
        code = ''.join(code)

        print('code:', code)
        user_params = session['user_params']
        number = user_params['country_code'] + user_params['phone_number']
        verification_check = client.verify.v2.services(VERIFY_SERVICE_SID).verification_checks.create(to=number, code=code)
        
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
            # incorrect code
            print("Incorrect code entered")
            flash("Incorrect verification code.", category="error")
            return render_template('verify.html', user=current_user)
        
@auth.route('/logout')
@login_required  # makes sure the user is logged in to see the logout page
def logout():
    logout_user()  # logs the current user out
    return redirect(url_for("auth.login"))