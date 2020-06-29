import json

from bson import json_util

from tests.BaseTestCase import BaseTestCase


class TestRating(BaseTestCase):

    """
    test request with form data
    """

    def test_rating_with_form_data(self):
        # init database
        self.createSongs()

        # get one song for testing
        song = self.db.songs.find_one({"title": "Awaki-Waki"})

        response = self.client.post(
            "/songs/rating", content_type="form-data", data={"song_id": song["_id"], "rating": 4})

        # result
        want = "request is not sent via json"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(got, want)

    """
    test request without required data
    """

    def test_rating_without_required_data(self):
        # init database
        self.createSongs()

        response = self.client.post(
            "/songs/rating", content_type="application/json", data=json.dumps({"x": "x"}))

        # result
        want = "missing parameter"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(got, want)

    """
    test request with invalid song id
    """

    def test_rating_with_invalid_song_id(self):
        # init database
        self.createSongs()

        response = self.client.post(
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

    def test_rating_with_invalid_rating(self):
        # init database
        self.createSongs()

        # get one song for testing
        song = self.db.songs.find_one({"title": "Awaki-Waki"})

        response = self.client.post(
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

    def test_rating_with_non_existing_song(self):
        # init database
        self.createSongs()

        response = self.client.post(
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

    def test_rating_with_existing_song(self):
        # init database
        self.createSongs()

        # get one song for testing
        song = self.db.songs.find_one({"title": "Awaki-Waki"})

        response = self.client.post(
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
