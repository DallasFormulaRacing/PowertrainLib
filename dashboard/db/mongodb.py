from flask import current_app, g
from pymongo import MongoClient
from werkzeug.local import LocalProxy
import os 
import sys

def get_db():
    mongo = getattr(g, '_database', None)
    if mongo is None:
        kw = {}
        # windows only
        if sys.platform == 'win32':
            import certifi
            kw['tlsCAFile'] = certifi.where()
        mongo = g._database = MongoClient(os.getenv('MONGO_URI'), **kw)
        
        # test connection
        mongo['cluster0'].list_collection_names()
    return mongo['cluster0']

db = LocalProxy(get_db)

def get_data(session_id):
    return list(db.realtime_metrics.find({'session_id': session_id}))