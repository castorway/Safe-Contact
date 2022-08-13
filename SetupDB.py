from pymongo import MongoClient

def Create_indexes(db):
    db["Users"].create_index([("Email","hashed")])
    db["Users"].create_index([("Phone","hashed")])

def main():
    Collection_Names = ["Users"]
    Port = ""
    Client = MongoClient(Port)
    Db = Client["DB"]
    Create_indexes()

if __name__ == "__main__":
    main()
