from pymongo import MongoClient
import os


def init():
    mongoUrl = ""
    if os.environ.get("ENV") == "development":
        mongoUrl = "mongodb://localhost:27017"
    else:
        mongoUrl = os.environ.get("MONGOURI")

    client = MongoClient(mongoUrl)
    return client


def base():
    client = init()
    database = client['venera']
    return database


def collection():
    database = base()
    collection = database['data']
    return collection


def ping():
    client = init()
    db = client.test_database
    return db.command("ping")
