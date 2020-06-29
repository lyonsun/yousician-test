import os

from dotenv import load_dotenv
load_dotenv()


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    MONGO_URI = "mongodb://{}:{}@mongodb:27017/{}?authSource=admin".format(
        os.getenv("MONGO_USERNAME"), os.getenv("MONGO_PASSWORD"), os.getenv("MONGO_DBNAME"))


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    MONGO_URI = "mongodb://{}:{}@mongodb:27017/{}?authSource=admin".format(
        os.getenv("MONGO_USERNAME"), os.getenv("MONGO_PASSWORD"), os.getenv("MONGO_TESTING_DBNAME"))
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
