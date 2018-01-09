import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret key!'
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')


class DevelopmentConfig(Config):
    MONGO_URI = os.environ.get('DEV_MONGODB_CONNECTION_STRING')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SPOTIFY_CALLBACK_URL = 'http://localhost:5000/callback/spotify'


class ProductionConfig(Config):
    MONGO_URI =  os.environ.get('MONGODB_URI')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SPOTIFY_CALLBACK_URL = 'https://playlist-pattern-scraper.herokuapp.com/callback/spotify'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
