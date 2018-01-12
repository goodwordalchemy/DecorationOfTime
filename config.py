import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret key!'
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')


class DevelopmentConfig(Config):
    MONGO_URI = os.environ.get('DEV_MONGODB_CONNECTION_STRING')
    SPOTIFY_CALLBACK_URL = 'http://localhost:5000/callback/spotify'


class ProductionConfig(Config):
    MONGO_URI =  os.environ.get('MONGODB_URI')
    SPOTIFY_CALLBACK_URL = 'https://decoration-of-time.herokuapp.com/callback/spotify'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
