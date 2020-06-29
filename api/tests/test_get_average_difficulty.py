import json

from tests.BaseTestCase import BaseTestCase


class TestGetAverageDifficulty(BaseTestCase):

    """
    test get average difficulty for all songs
    """

    def test_get_average_difficulty_for_all_songs(self):
        # init database
        self.createSongs()

        response = self.client.get("/songs/avg/difficulty",
                                   headers={"Content-Type": "application/json"})

        # result
        want = (14.6+9.1+15)/3
        got = next(iter(json.loads(response.data)))["average_difficulty"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got, want)

    """
    test get average difficulty for certain level only
    """

    def test_get_average_difficulty_for_songs_in_certain_level(self):
        # init database
        self.createSongs()

        response = self.client.get("/songs/avg/difficulty?level=13",
                                   headers={"Content-Type": "application/json"})

        # result
        want = (14.6+15)/2
        got = next(iter(json.loads(response.data)))["average_difficulty"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got, want)
