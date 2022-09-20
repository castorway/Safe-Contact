Safe Contact is here to help you worry less when your friend is out late, your child is going on their first trip, or you are working in an isolated area alone but need supervision. Make an account to keep in touch with your friends and family automatically using Twilio SMS messages. They can also share their last location with you with the click of one button!

Having a safe contact while you are in a dangerous location is especially of importance to women and many visible minorities. Safe Contact is here to help you stay connected with your friends and family automatically. With an easy-to-use interface, users can share their location and reply to Twilio texts to keep contacts updated on their current whereabouts!

### Accomplishments that we're proud of

The team is very proud of the visuals present in this web application, we went for a minimal yet effective look. Considering the fact that we were a group of three, we are really proud of the complexity of our project and the various tools we brought together to build Safe Contact. The long list of functionality that we added to this project includes lots of Twilio integration for SMS services (both messaging and verification), map API integration, and two-way messaging. To increase the safety aspect for the users, we also included location tracking if they give permission.

### What's next for Safe Contact

We are looking to host the website on a more permanent domain while transferring to a cloud-based database like MongoDB. To create a more established software cycle, we want to enable pipelines to perform testing and continuous deployment of code through GitHub Actions.

### Challenges

* We encountered difficulties when implementing the location sharing feature. Using the Leaflet.js library, the Google Maps API, and HTML Geolocation API took quite some time to integrate with the logic of our app.
* We faced Twilio errors when testing our application which slowed down our development cycle.

### Instructions

This webapp requires API/authentication keys for Twilio and ngrok to run correctly, as well as a verification service to be set up on the corresponding Twilio account. [ngrok](https://ngrok.com/) must also be installed.

File configuration requirements:

- `ngrok.exe` should be in the `HackAlpha` directory.
- `.env` should be in the `HackAlpha` directory, and contain the variables VERIFY_SERVICE_SID, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_NUMBER.

Twilio requirements:

- A Verify Service should be set up on the Twilio account with access to SMS verification, and VERIFY_SERVICE_SID should use the SID for this service.
- The Twilio phone number should be specified in the `.env` file.
- The Messaging POST webhook for the Twilio phone number should be set to the webhook created by ngrok after `start.sh` is run.

ngrok requirements:

- ngrok must be authenticated, as described [here](https://dashboard.ngrok.com/get-started/your-authtoken).

Run `source start.sh` to start the application if all keys and tokens are in the correct places.
