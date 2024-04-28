from pymongo import MongoClient
import environ

from quotes.quotes.settings import env

client = None

def get_mongodb():
    global client
    if client is None:
        client = MongoClient(env('MONGO'))
    db = client.test
    return db
