import unittest
import json
import os

from bson import json_util, objectid
from flask_pymongo import MongoClient, ObjectId

from app import app, db


class Tests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def createSongs(self):
        sample_data = [
            {
                "artist": "The Yousicians",
                "title": "Lycanthropic Metamorphosis",
                "difficulty": 14.6,
                "level": 13,
                "released": "2016-10-26"
            },
            {
                "artist": "The Yousicians",
                "title": "A New Kennel",
                "difficulty": 9.1,
                "level": 9,
                "released": "2010-02-03"
            },
            {
                "artist": "Mr Fastfinger",
                "title": "Awaki-Waki",
                "difficulty": 15,
                "level": 13,
                "released": "2012-05-11"
            }
        ]
        self.db.songs.insert_many(sample_data)

    """
    test if database was empty before other tests
    """

    def testEmptyDatabase(self):
        got = json.loads(json_util.dumps(self.db.songs.find()))
        want = []

        self.assertEqual(got, want)

    """
    test get endpoint to root route
    """

    def testHello(self):
        # request
        response = self.app.get(
            "/", headers={"Content-Type": "application/json"})

        # result
        self.assertEqual(response.data, b'{"Hello": "world"}')
        self.assertEqual(response.status_code, 200)

    """
    test get endpoint for fetching all songs
    """

    def test_get_all_songs(self):
        # init database
        self.createSongs()

        """
        test get all songs
        """
        response = self.app.get(
            "/songs", headers={"Content-Type": "application/json"})

        # result
        want = 3
        got = len(json.loads(response.data))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got, want)

        """
        test get songs for certain page only
        """
        response = self.app.get(
            "/songs?page=2&per_page=2", headers={"Content-Type": "application/json"})

        # result
        want_len = 1
        got_len = len(json.loads(response.data))

        want_first_data_title = "Awaki-Waki"
        got_first_data_title = next(iter(json.loads(response.data)))["title"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got_len, want_len)
        self.assertEqual(want_first_data_title, got_first_data_title)

    """
    test get endpoint for fetching average difficulty
    """

    def test_get_average_difficulty(self):
        # init database
        self.createSongs()

        """
        test get average difficulty for all songs
        """
        response = self.app.get("/songs/avg/difficulty",
                                headers={"Content-Type": "application/json"})

        # result
        want = (14.6+9.1+15)/3
        got = next(iter(json.loads(response.data)))["average_difficulty"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got, want)

        """
        test get average difficulty for certain level only
        """
        response = self.app.get("/songs/avg/difficulty?level=13",
                                headers={"Content-Type": "application/json"})

        # result
        want = (14.6+15)/2
        got = next(iter(json.loads(response.data)))["average_difficulty"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got, want)

    """
    test get endpoint for searching songs
    """

    def test_search_songs(self):
        # init database
        self.createSongs()

        """
        test search songs when required parameter is missing
        """
        response = self.app.get(
            "/songs/search", headers={"Content-Type": "application/json"})

        # result
        want = "missing parameter"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(got, want)

        """
        test search songs with required parameter
        """
        response = self.app.get(
            "/songs/search?message=yousician", headers={"Content-Type": "application/json"})

        # result
        data = json.loads(response.data)
        want_len = 2
        got_len = len(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got_len, want_len)

    """
    test post endpoint for adding a rating for a song
    """

    def test_rating(self):
        # init database
        self.createSongs()

        # get one song for testing
        song = self.db.songs.find_one({"title": "Awaki-Waki"})

        """
        test request with form data
        """
        response = self.app.post(
            "/songs/rating", content_type="form-data", data={"song_id": song["_id"], "rating": 4})

        # result
        want = "request is not sent via json"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(got, want)

        """
        test request without required data
        """
        response = self.app.post(
            "/songs/rating", content_type="application/json", data=json.dumps({"x": "x"}))

        # result
        want = "missing parameter"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(got, want)

        """
        test request with invalid song id
        """
        response = self.app.post(
            "/songs/rating", content_type="application/json",
            data=json.dumps({"song_id": "x", "rating": 4}))

        # result
        want = "song id is not valid"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(got, want)

        """
        test request with invalid rating
        """
        response = self.app.post(
            "/songs/rating", content_type="application/json",
            data=json.dumps({"song_id": str(song["_id"]), "rating": 40}))

        # result
        want = "rating should be between 1 and 5"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(got, want)

        """
        test request with non existing song
        """
        response = self.app.post(
            "/songs/rating", content_type="application/json",
            data=json.dumps({"song_id": "555555555555555555555555", "rating": 4}))

        # result
        want = "song is not found"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 404)
        self.assertEqual(got, want)

        """
        test request with existing song
        """
        response = self.app.post(
            "/songs/rating", content_type="application/json",
            data=json.dumps({"song_id": str(song["_id"]), "rating": 4}))

        ratings = json.loads(json_util.dumps(
            self.db.ratings.find({"song_id": str(song["_id"])})))

        # result
        want_len = 1
        got_len = len(ratings)
        want_rating = 4
        got_rating = next(iter(ratings))["rating"]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(got_len, want_len)
        self.assertEqual(got_rating, want_rating)

    """
    test get endpoint for fetching ratings for a song
    """

    def test_get_ratings(self):
        # init database
        self.createSongs()

        """
        test request with invalid song id
        """
        response = self.app.get("/songs/avg/rating/x",
                                content_type="application/json")

        # result
        want = "song id is not valid"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(got, want)

        """
        test request with non existing song
        """
        response = self.app.get(
            "/songs/avg/rating/5ef63cc331a5cd25e9971b4e", content_type="application/json")

        # result
        want = "song is not found"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 404)
        self.assertEqual(got, want)

        """
        test request with existing song but no ratings
        """
        # get one song for testing
        song = self.db.songs.find_one({"title": "Awaki-Waki"})

        response = self.app.get(
            "/songs/avg/rating/{}".format(str(song["_id"])), content_type="application/json")

        # result
        want = "no ratings for this song"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 404)
        self.assertEqual(got, want)

        """
        test request with existing song having a number of ratings
        """
        # get one song for testing
        song = self.db.songs.find_one({"title": "Awaki-Waki"})

        # create ratings for the song
        self.db.ratings.insert_many([
            {"song_id": str(song["_id"]), "rating": 3},
            {"song_id": str(song["_id"]), "rating": 3},
            {"song_id": str(song["_id"]), "rating": 4},
            {"song_id": str(song["_id"]), "rating": 5},
        ])

        response = self.app.get(
            "/songs/avg/rating/{}".format(str(song["_id"])), content_type="application/json")

        rating = next(iter(json.loads(response.data)))

        # result
        want_avg = (3+3+4+5)/4
        got_avg = rating["average"]
        want_highest = 5
        got_highest = rating["highest"]
        want_lowest = 3
        got_lowest = rating["lowest"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got_avg, want_avg)
        self.assertEqual(got_highest, want_highest)
        self.assertEqual(got_lowest, want_lowest)

    def tearDown(self):
        self.db.songs.drop()
        self.db.ratings.drop()


if __name__ == "__main__":
    unittest.main()
