import json

from tests.BaseTestCase import BaseTestCase


class TestGetAllSongs(BaseTestCase):

    """
    test get all songs
    """

    def test_get_all_songs(self):
        # init database
        self.createSongs()
        response = self.client.get(
            "/songs", headers={"Content-Type": "application/json"})

        # result
        want = 3
        got = len(json.loads(response.data))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got, want)

    """
    test get songs for certain page only
    """

    def test_get_all_songs_with_pagination(self):
        # init database
        self.createSongs()

        response = self.client.get(
            "/songs?page=2&per_page=2", headers={"Content-Type": "application/json"})

        # result
        want_len = 1
        got_len = len(json.loads(response.data))

        want_first_data_title = "Awaki-Waki"
        got_first_data_title = next(iter(json.loads(response.data)))["title"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(got_len, want_len)
        self.assertEqual(want_first_data_title, got_first_data_title)
