import os
import re

from gwa_spotify_api import SpotifyAuthAPI

from config import SPOTIFY_API_CONFIG

PLAYLIST_PATTERNS = [
    r'My Shazam Tracks',
    r'Your Top Songs \d{4}',
    r'The Ones That Got Away',
    r'Your Summer Rewind',
    r'Discover Weekly',
]


def _matches_playlist_patterns(playlist_name):
    for pattern in PLAYLIST_PATTERNS:
        if re.match(pattern, playlist_name):
            return True
    return False

def _get_user_filename(user_id):
    return os.path.join('data', user_id)

spotify_api = SpotifyAuthAPI(config=SPOTIFY_API_CONFIG)

me_id = spotify_api.get('me')['id']

user_playlists = spotify_api.get('me/playlists')


playlist_info_dicts = [{
    'id': p['id'],
    'name': p['name'],
    'owner_id': p['owner']['id']
} for p in user_playlists if _matches_playlist_patterns(p['name'])]


for playlist_info_dict in playlist_info_dicts:

    playlist_tracks = spotify_api.get('users/{me_id}/playlists/{playlist_id}/tracks'.format(
        me_id=playlist_info_dict['owner_id'],
        playlist_id=playlist_info_dict['id']
    ))
    playlist_tracks = [t['track'] for t in playlist_tracks]

    track_info_dicts = [{
        'id': t['id'],
        'name': t['name'],
        'artist1_id': t['artists'][0]['id'],
        'artist1_name': t['artists'][0]['name'],
        'album_id': t['album']['id'],
        'album_name': t['album']['name'],
    } for t in playlist_tracks]

    playlist_info_dict['tracks'] = track_info_dicts

    print(playlist_info_dict)

with open(_get_user_filename(me_id), 'w') as handle:
    pickle.dump(playlist_info_dicts, handle)

