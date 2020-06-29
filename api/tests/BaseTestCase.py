import unittest

from app import app, db


class BaseTestCase(unittest.TestCase):

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

    def tearDown(self):
        self.db.songs.drop()
        self.db.ratings.drop()


if __name__ == "__main__":
    unittest.main()
