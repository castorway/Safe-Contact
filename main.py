from client import create_app
from pymongo import MongoClient
import json
import flask
import hashlib

# make the web app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # run the web app and update on every save