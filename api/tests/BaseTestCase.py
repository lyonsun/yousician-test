import unittest

from app import create_app
from db import mongo


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.db = mongo.db

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

    def tearDown(self):
        self.db.songs.drop()
        self.db.ratings.drop()


if __name__ == "__main__":
    unittest.main()
