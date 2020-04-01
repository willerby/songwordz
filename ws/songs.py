import musicbrainzngs as mb
from config import Config
from ws.transport import Results


mb.set_useragent(*Config.user_agent)


def call_works(ps_artist_id, pi_limit, pi_offset=None):
    """
        queries the MB webservice for works
    :param ps_artist_id: Musicbrainz MBID for required artists
    :param pi_limit: max number of entries per call
    :param pi_offset: pagination offset
    :return: Results object containing dict of works, or diagnostics if error occurred
    """
    try:
        o_result = Results(pd_results=mb.browse_works(artist=ps_artist_id, limit=pi_limit, offset=pi_offset))
    except mb.WebServiceError as e:
        o_result = Results(ps_error=f'Web Service error encountered: {repr(e)}')
    except Exception as e:
        o_result = Results(ps_error=f'Unexpected error encountered: {repr(e)}')
    return o_result


def song_list(ps_artist_id):
    """
        Call Musicbrainz using the 'works' entity to return a list of songs for a predetermined artist.
    :param ps_artist_id: Musicbrainz MBID for required artists
    :return: Results object containing list of songs by artist (de-duped), or diagnostics if error occurred
    """
    l_works = []
    i_limit = 100  # mb max value
    i_offset = 0

    # Make initial call, then check if further calls required
    o_works = call_works(ps_artist_id=ps_artist_id, pi_limit=i_limit)
    if not o_works.b_error:
        l_works += o_works.d_result.get('work-list')
        i_work_count = o_works.d_result.get('work-count') or 0

        if i_work_count > len(l_works):
            while len(l_works) < i_work_count and not o_works.b_error:
                i_offset += i_limit
                o_works = call_works(ps_artist_id=ps_artist_id, pi_limit=i_limit, pi_offset=i_offset)
                if not o_works.b_error:
                    l_works += o_works.d_result.get('work-list')

    if o_works.b_error:
        o_result = Results(ps_error=o_works.s_error_message)
    else:
        o_result = Results(pl_results=list(set([work['title'] for work in l_works if work.get('type') == 'Song' and 'title' in work])))

    return o_result
