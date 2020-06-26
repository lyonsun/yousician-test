import os
import json

from bson import json_util, objectid

from flask import Flask, jsonify, request
from flask_pymongo import MongoClient, ObjectId
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mongo_uri = "mongodb://{}:{}@mongodb:27017/?authSource=admin".format(
    os.getenv("MONGO_USERNAME"), os.getenv("MONGO_PASSWORD"))
client = MongoClient(mongo_uri)
db = client.music


@app.route("/")
def hello():
    return {"Hello": "world"}


@app.route("/songs", methods=["GET"])
# - GET /songs
#   - Returns a list of songs with some details on them
#   - Add possibility to paginate songs.
def get_all_songs():
    # check if pagination parameters are given
    if "page" in request.args and "per_page" in request.args:
        page = request.args.get("page")
        per_page = request.args.get("per_page")
        offset = ((int(page) - 1) * int(per_page)) if int(page) > 0 else 0

        cursor = db.songs.find().skip(offset).limit(int(per_page))
    else:
        cursor = db.songs.find()

    # find songs
    songs_collection = json.loads(json_util.dumps(cursor))
    return jsonify(songs_collection)


@app.route("/songs/avg/difficulty", methods=["GET"])
# - GET /songs/avg/difficulty
#   - Takes an optional parameter "level" to select only songs from a specific level.
#   - Returns the average difficulty for all songs.
def get_average_difficulty():
    # check if optional parameter is given, query with or without optional parameter condition
    if "level" in request.args:
        level = int(request.args.get("level"))
        cursor = db.songs.aggregate([
            {"$match": {"level": level}},
            {"$group": {
                "_id": None,
                "average_difficulty": {"$avg": "$difficulty"}
            }}
        ])
    else:
        cursor = db.songs.aggregate([
            {"$group": {
                "_id": None,
                "average_difficulty": {"$avg": "$difficulty"}
            }}
        ])

    songs_collection = list(cursor)
    return jsonify(songs_collection)


@app.route("/songs/search", methods=["GET"])
# - GET /songs/search
#   - Takes in parameter a "message" string to search.
#   - Return a list of songs. The search should take into account song"s artist and title.
#     The search should be case insensitive.
def search_songs():
    # check if parameter exist
    if "message" in request.args:
        message = request.args.get("message")

        # find songs
        db.songs.create_index([("artist", "text"), ("title", "text")])
        cursor = db.songs.find({"$text": {"$search": message}})
        songs_collection = json.loads(json_util.dumps(cursor))

        return jsonify(songs_collection)
    else:
        return jsonify({"error": "missing parameter"})


@app.route("/songs/rating", methods=["POST"])
# - POST /songs/rating
#   - Takes in parameter a "song_id" and a "rating"
#   - This call adds a rating to the song. Ratings should be between 1 and 5.
def rating():
    # check if request data is json
    if not request.json:
        return jsonify({"error": "request is not sent via json"})

    params = request.get_json(force=True)

    # check if song id is given
    if "song_id" not in params or "rating" not in params:
        return jsonify({"error": "missing parameter"})

    song_id = params["song_id"]
    rating = params["rating"]

    # check if song id is valid
    if objectid.ObjectId.is_valid(song_id) == False:
        return jsonify({"error": "song id is not valid"})

    # check if rating is in correct range
    if rating < 1 or rating > 5:
        return jsonify({"error": "rating should be between 1 and 5"})

    # find the song
    song = json.loads(json_util.dumps(
        db.songs.find({"_id": ObjectId(song_id)})))
    if not song:
        return jsonify({"error": "song is not found"})

    # update song with rating
    inserted_id = db.ratings.insert_one(
        {"song_id": song_id, "rating": rating}).inserted_id

    # get the rating
    rating = json.loads(json_util.dumps(
        db.ratings.find({"_id": inserted_id})))

    return jsonify(rating)


@app.route("/songs/avg/rating/<song_id>", methods=["GET"])
# - GET /songs/avg/rating/<song_id>
#   - Returns the average, the lowest and the highest rating of the given song id.
def get_ratings(song_id):
    # check if song id is valid
    if objectid.ObjectId.is_valid(song_id) == False:
        return jsonify({"error": "song id is not valid"})

    # find the song
    song = json.loads(json_util.dumps(
        db.songs.find({"_id": ObjectId(song_id)})))
    if not song:
        return jsonify({"error": "song is not found"})

    # get result
    cursor = db.ratings.aggregate([
        {"$match": {"song_id": song_id}},
        {"$group": {
            "_id": None,
            "average": {"$avg": "$rating"},
            "highest": {"$max": "$rating"},
            "lowest": {"$min": "$rating"}
        }}
    ])
    ratings = list(cursor)

    if not ratings:
        return jsonify({"error": "no ratings for this song"})

    return jsonify(ratings)


if __name__ == "__main__":
    app.run()
