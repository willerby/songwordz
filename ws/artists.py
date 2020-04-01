import musicbrainzngs as mb
from config import Config
from ws.transport import Results


mb.set_useragent(*Config.user_agent)


def search_artists(ps_artist_name):
    """
        Calls the Musicbrainz web service (via musicbrainzngs) to retrieve a list of artists
    :param ps_artist_name: artist name
    :return: Results object containing a list of candidate artists
    """
    l_artists = []
    try:
        o_artists = Results(pd_results=mb.search_artists(ps_artist_name))
    except mb.WebServiceError as e:
        o_artists = Results(ps_error=f'Web Service error encountered: {repr(e)}')
    except Exception as e:
        o_artists = Results(ps_error=f'Unexpected error encountered: {repr(e)}')

    if not o_artists.b_error and len(o_artists.d_result['artist-list']) > 0:
        # refine artist results
        i_max_artists = Config.max_artists_to_list
        for idx in range(0, min(i_max_artists, len(o_artists.d_result['artist-list']))):
            l_artists.append({'id': o_artists.d_result['artist-list'][idx]['id'],
                              'name': o_artists.d_result['artist-list'][idx]['name'],
                              'score': o_artists.d_result['artist-list'][idx].get('ext:score'),
                              'type': o_artists.d_result['artist-list'][idx].get('type'),
                              'country': o_artists.d_result['artist-list'][idx].get('country'),
                              'tags': [tag['name'] for tag in o_artists.d_result['artist-list'][idx].get('tag-list') or []]})

    if o_artists.b_error:
        o_result = Results(ps_error=o_artists.s_error_message)
    else:
        o_result = Results(pl_results=l_artists)
    return o_result
