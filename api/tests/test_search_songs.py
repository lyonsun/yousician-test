import json

from tests.BaseTestCase import BaseTestCase


class TestSearchSongs(BaseTestCase):

    """
    test search songs when required parameter is missing
    """

    def test_search_songs_without_required_params(self):
        # init database
        self.createSongs()

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

    def test_search_songs_with_required_params(self):
        # init database
        self.createSongs()

        response = self.app.get(
            "/songs/search?message=yousician", headers={"Content-Type": "application/json"})

        # result
        data = json.loads(response.data)
        want_len = 2
        got_len = len(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got_len, want_len)
