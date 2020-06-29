import json

from bson import json_util

from tests.BaseTestCase import BaseTestCase


class TestDatabase(BaseTestCase):

    """
    test if database was empty before other tests
    """

    def testEmptyDatabase(self):
        got = json.loads(json_util.dumps(self.db.songs.find()))
        want = []

        self.assertEqual(got, want)
