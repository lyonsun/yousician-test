import os
import json

from bson import json_util

from flask import Flask, jsonify
from flask_pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mongo_uri = "mongodb://{}:{}@mongodb:27017/?authSource=admin".format(
    os.getenv("MONGO_USERNAME"), os.getenv("MONGO_PASSWORD"))
client = MongoClient(mongo_uri)
db = client.music


@app.route('/')
def hello():
    return {"Hello": "world"}


@app.route('/songs', methods=["GET"])
def get_all_songs():

    songs_collection = json.loads(json_util.dumps(db.songs.find()))
    return jsonify(songs_collection)


if __name__ == "__main__":
    app.run()
