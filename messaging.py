import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
# email verification with twilio, and environment variables to safely store our API keys

from datetime import datetime, timedelta


load_dotenv()
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID = os.environ.get('VERIFY_SERVICE_SID')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


client = Client(os.environ['TWILIO_SID'], os.environ['TWILIO_AUTH'])

# #TODO: change this once done testing
# # minute tolerance for checking older reminders
# TOLERANCE = 10
# DEBUG = True

# def send_reminders(scheduler, message):
#     with scheduler.app.app_context():
#         #print("------------- the time is...", datetime.now(), flush=True)

#         now = datetime.now()

#         this_time = now.time()
#         earlier_time = (now - timedelta(minutes=TOLERANCE)).time()
#         #print(this_time, earlier_time)

#         # get reminder/session instance
#         reminders = Reminder.query.filter(Reminder.time <= this_time)
#         reminders = reminders.filter(Reminder.time >= earlier_time)

#         if DEBUG: print("send_reminders called", flush=True)

#         for rem in reminders:
#             if DEBUG: print(">", rem, rem.time, flush=True)

#             if rem.lastnotif < now.date():
#                 # a reminder hasn't been sent yet today
#                 if DEBUG: print('>> havent reminded yet today; texting', rem, flush=True)
                
#                 # get user's phone number
#                 phone = rem.user.phone

#                 if phone:
#                     msg = f"{rem.name} [{rem.dosage}]\n{rem.notes}"
#                     try:
#                         client.messages.create(to=phone, from_="+15878585813", body=msg)
#                     except TwilioRestException:
#                         print(f">> Unverified phone number for user {rem.user.id}, couldn't send message.")
#                 elif DEBUG:
#                     print(f"No phone specified for user {rem.user.id}.", flush=True)
                
#                 # set 'lastnotif' to today so we know not to text again today
#                 rem.lastnotif = now.date()

#         db.session.commit()


def send_verification(number):
    """ Send SMS verification code using Twilio
    """
    ver = client.verify.v2.services(VERIFY_SERVICE_SID).verification_checks.create(to=number, channel='sms')

    print(ver.status)
    return ver

def check_verification(number, code):
    """ Check SMS verification code using Twilio
    """
    ver = client.verify.v2.services(VERIFY_SERVICE_SID).verification_checks.create(to='+15017122661', code='123456')
    return check.status == 'approved'
