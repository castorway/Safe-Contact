import os
from twilio.rest import Client
from dotenv import load_dotenv


# set up twilio api keys
load_dotenv()
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID = os.environ.get('VERIFY_SERVICE_SID')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# service = client.verify.services.create(friendly_name='safecontact_verify_service')
# print('Verification service ID: '+service.sid)

verification_check = client.verify.v2.services(VERIFY_SERVICE_SID).verification_checks.create(to='+18254365663', code='442634')

print(verification_check.status)