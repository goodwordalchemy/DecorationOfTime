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



def scrape_user_playlists(spotify_api):
    user_playlists = spotify_api.get('me/playlists')

    playlist_info_dicts = [{
        'id': p['id'],
        'name': p['name'],
        'owner_id': p['owner']['id']
    } for p in user_playlists if _matches_playlist_patterns(p['name'])]


    for playlist_info_dict in playlist_info_dicts:

        playlist_tracks = spotify_api.get('users/{owner_id}/playlists/{playlist_id}/tracks'.format(
            owner_id=playlist_info_dict['owner_id'],
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

    me_id = spotify_api.get('me')['id']

    output = {
        'user_id': me_id,
        'playlists': playlist_info_dicts
    }

    return output


def user_playlists_to_str(user_playlists):
    playlist_info_dicts = user_playlists['playlists']

    output = ''

    output += '{}\n'.format(user_playlists['user_id'])

    for playlist_info in playlist_info_dicts:
        output += '{playlist_id},{playlist_name}\n'.format(
            playlist_id=playlist_info['id'],
            playlist_name=playlist_info['name']
        )

        for track_info in playlist_info['tracks']:
            output += '{track_id},{track_name},{artist1_id},{artist1_name},{album_id},{album_name}\n'.format(
                track_id=track_info['id'], track_name=track_info['name'],
                artist1_id=track_info['artist1_id'], artist1_name=track_info['artist1_name'],
                album_id=track_info['album_id'], album_name=track_info['album_name']
            )

        output += '\n'

    return output




if __name__ == '__main__':
    spotify_api = SpotifyAuthAPI(config=SPOTIFY_API_CONFIG)

    user_playlists = scrape_user_playlists(spotify_api)

    playlists_str = user_playlists_to_str(user_playlists)

    print(playlists_str)
