'''
# Playlist Pattern Scraper

This app allows people who give me permission to scrape the track data from playlists matching any of the following patterns:

    My Shazam Tracks
    Your Top Songs <year>
    The Ones That Got Away
    Your Summer Rewind
    Discover Weekly

## How it works

1. User arrives at home page.
2. User Oauths into Spotify
3. App scrapes playlists matching patterns listed above.  It puts the track metadata and track-playlist links into a database.
4. User arrives at "Thank You" screen.

## What I will do with the data

1. I will smile ear to ear and comb through the collections of people that I already know to have outstanding taste in music.
2. I will practice implementing music recommendation algorithms and clustering algorithms.

## What does the user get out of this?

1. A personalized playlist of music recommendations based on the music of other users who have similar taste in music.
2. The satisfaction of knowing you have allowed me to learn and discover tons of great music.
'''
import os
from flask import Flask, redirect, render_template, request, url_for
from flask_login import current_user, login_user, LoginManager, login_required, logout_user, UserMixin
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from gwa_spotify_api import SpotifyAuthAPI
from rauth import OAuth2Service

from config import config
from scrape_user_playlists import scrape_user_playlists, user_playlists_to_str


SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'

SCOPES = [
    'playlist-read-private',
    'user-top-read',
]

'''
The `ENVIRONMENT_NAME` needs to be set to 'production' or else it defaults
to 'development'
'''
config_name = os.environ.get('ENVIRONMENT_NAME') or 'development'

app = Flask(__name__)
app.config.from_object(config[config_name])

db = SQLAlchemy(app)
mongo = PyMongo(app)
lm = LoginManager(app)


spotify_api_config = {
    'SPOTIFY_CLIENT_ID': app.config['SPOTIFY_CLIENT_ID'],
    'SPOTIFY_CLIENT_SECRET': app.config['SPOTIFY_CLIENT_SECRET'],
    'SPOTIFY_CALLBACK_URL': app.config['SPOTIFY_CALLBACK_URL'],
}
spotify_api = SpotifyAuthAPI(assign_token=False, config=spotify_api_config, scopes_list=SCOPES)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    display_name = db.Column(db.String(64))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))



@app.route('/authorize/spotify')
def spotify_authorize():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    authorize_url = spotify_api.get_authorize_url()

    return redirect(authorize_url)


@app.route('/callback/spotify')
def spotify_callback():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    auth_code = request.args['code']

    token = spotify_api.get_access_token(auth_code)
    spotify_api.assign_token(token=token)

    user_profile_info = spotify_api.get('me')
    social_id = user_profile_info['id']
    display_name = user_profile_info['display_name']

    user = User.query.filter_by(social_id=social_id).first()

    if not user:
        user = User(social_id=social_id, display_name=display_name)

        db.session.add(user)
        db.session.commit()

    login_user(user, True)

    return redirect(url_for('spotify_scrape_data'))


@app.route('/scrape_data/spotify')
@login_required
def spotify_scrape_data():
    user_playlists = scrape_user_playlists(spotify_api)

    user = mongo.db.users.find_one({'user_id': user_playlists['user_id']})
    if not user:
        result = mongo.db.users.insert_one(user_playlists)
        print('inserted one item with id: {}'.format(result.inserted_id))
    else:
        print('user already exists')

    return redirect(url_for('welcome'))


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html'),
