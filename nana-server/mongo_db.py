from flask import g
from pymongo import MongoClient

def get_db():
    if not hasattr(g, "db"):
        client = MongoClient('localhost', 27017)
        g.db = client.nana
    return g.db