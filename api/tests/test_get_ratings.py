import json

from bson import json_util

from tests.BaseTestCase import BaseTestCase


class TestGetRatings(BaseTestCase):

    """
    test request with invalid song id
    """

    def test_get_ratings_with_invalid_song_id(self):
        # init database
        self.createSongs()
        response = self.client.get("/songs/avg/rating/x",
                                   content_type="application/json")

        # result
        want = "song id is not valid"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(got, want)

    """
    test request with non existing song
    """

    def test_get_ratings_with_non_existing_song(self):
        # init database
        self.createSongs()

        response = self.client.get(
            "/songs/avg/rating/5ef63cc331a5cd25e9971b4e", content_type="application/json")

        # result
        want = "song is not found"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 404)
        self.assertEqual(got, want)

    """
    test request with existing song but no ratings
    """

    def test_get_ratings_with_existing_song_but_no_ratings(self):
        # init database
        self.createSongs()

        # get one song for testing
        song = self.db.songs.find_one({"title": "Awaki-Waki"})

        response = self.client.get(
            "/songs/avg/rating/{}".format(str(song["_id"])), content_type="application/json")

        # result
        want = "no ratings for this song"
        got = json.loads(response.data)["error"]

        self.assertEqual(response.status_code, 404)
        self.assertEqual(got, want)

    """
    test request with existing song having a number of ratings
    """

    def test_get_ratings_with_existing_song_having_ratings(self):
        # init database
        self.createSongs()

        # get one song for testing
        song = self.db.songs.find_one({"title": "Awaki-Waki"})

        # create ratings for the song
        self.db.ratings.insert_many([
            {"song_id": str(song["_id"]), "rating": 3},
            {"song_id": str(song["_id"]), "rating": 3},
            {"song_id": str(song["_id"]), "rating": 4},
            {"song_id": str(song["_id"]), "rating": 5},
        ])

        response = self.client.get(
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
