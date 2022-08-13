from datetime import datetime, timedelta
from .models import Connections, User
from . import db
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

#TODO: change this once done testing
# minute tolerance for checking older conninders
TOLERANCE = 10
DEBUG = True

# load secret environment variables
load_dotenv()
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_texts(scheduler):
    ''' Goes through all the sessions and sends texts to the ones who have passed
        their interval time.
    '''
    if DEBUG: print("send_texts called", flush=True)

    with scheduler.app.app_context():
        print("------------- the time is...", datetime.now(), flush=True)

        now = datetime.now()

        this_time = now.time()
        earlier_time = (now - timedelta(minutes=TOLERANCE)).time()
        print(this_time, earlier_time)

        connections = Connections.query.filter(Connections.time <= this_time)
        connections = connections.filter(Connections.time >= earlier_time)

        for conn in connections:
            if DEBUG: print(">", conn, conn.last_text, conn.interval, this_time, flush=True)

            if conn.last_text + conn.interval < this_time:
                if DEBUG: print('>> havent texted yet; texting', conn, flush=True)
                
                # get user's phone number
                country_code = conn.user.country_code
                phone_number = conn.user.phone_number
                number = country_code + phone_number

                client.messages.create(to=number, from_="+15878585813", body=conn.text_contents)
                
                # set last time to now
                conn.last_text = this_time

        db.session.commit()
