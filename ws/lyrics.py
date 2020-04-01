import requests
import json
from config import Config
from ws.transport import Results


def retrieve_lyrics(ps_artist, po_songs):
    """
       Calls the lyrics.ovh webservice to return lyrics for a list of artist songs. Filters out null returns
    :param ps_artist: artist name
    :param po_songs: Results object containing list of artist songs
    :return: Results object containing list of lyrics
    """
    # TODO - asyncio? or would I get throttled?

    d_headers = {'Accept': 'application/json',
                 'User-Agent': " ".join(Config.user_agent)}
    l_lyrics = []
    o_result = None
    for song in po_songs.l_result:
        s_lyric_url = f'https://api.lyrics.ovh/v1/{requests.utils.quote(ps_artist)}/{requests.utils.quote(song)}'
        try:
            o_ws_result = requests.get(s_lyric_url,
                                       headers=d_headers)
            s_lyric = json.loads(o_ws_result.text).get('lyrics')
            if s_lyric and s_lyric.lower() != 'instrumental':
                l_lyrics.append({'song_title': song, 'lyrics': s_lyric})
        except requests.RequestException as e:
            o_result = Results(ps_error=f'Web Service error encountered: {repr(e)}')
        except Exception as e:
            o_result = Results(ps_error=f'Unexpected error encountered: {repr(e)}')

    if not o_result:
        o_result = Results(pl_results=l_lyrics)
    return o_result
