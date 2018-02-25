import os

from gwa_spotify_api import SpotifyAuthAPI


SCOPES = ['playlist-read-private', 'user-top-read']
TIME_RANGES = ['short_term', 'medium_term', 'long_term']


def _scrape_top_artists_or_tracks(spotify_api, a_or_t):
    result_dict = {}
    for time_range in TIME_RANGES:
        result_dict[time_range] = spotify_api.get(
            'me/top/' + a_or_t, params={
                'limit': 50,
                'time_range': time_range
            }
        )

    return result_dict

def scrape_favorites(spotify_api):
    favorite_artists = _scrape_top_artists_or_tracks(spotify_api, 'artists')
    favorite_tracks = _scrape_top_artists_or_tracks(spotify_api, 'tracks')

    return {
        'tracks': favorite_tracks,
        'artists': favorite_tracks,
    }

if __name__ == '__main__':
    spotify_api_config = {
        'SPOTIFY_CLIENT_ID': os.environ['SPOTIFY_CLIENT_ID'],
        'SPOTIFY_CLIENT_SECRET': os.environ['SPOTIFY_CLIENT_SECRET'],
        'SPOTIFY_CALLBACK_URL': os.environ['SPOTIFY_CALLBACK_URL'],
    }
    spotify_api = SpotifyAuthAPI(assign_token=True, scopes_list=SCOPES)

    print(spotify_api.get('me/top/artists'))
