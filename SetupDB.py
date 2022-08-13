from pymongo import MongoClient
import json

def Create_indexes(db):
    db["Users"].create_index([("Email","hashed")])
    db["Users"].create_index([("Phone","hashed")])