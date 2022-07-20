from flask import Flask
from datetime import datetime, timedelta
from bson import json_util, ObjectId
from flask_cors import CORS
from app.blueprint_api  import books_api_v1
from flask.json import JSONEncoder
import os

class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


app = Flask(__name__)
CORS(app)
app.json_encoder = MongoJsonEncoder
app.register_blueprint(books_api_v1)


@app.route('/<path:path>')
def serve(path):
    return "invalid path"
        

