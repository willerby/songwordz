from ws import artists, songs, lyrics
from config import Config
from tabulate import tabulate
from analysis import word_count
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


def request_artist_name():
    """
        CLI script to retrieve an artist name from user input
    :return: artist name
    """
    b_name_err = True
    s_artist_nm = None
    while b_name_err:
        s_artist_nm = input("Please enter the name of the artist: ")
        if s_artist_nm:
            if len(s_artist_nm) >= 3:
                b_name_err = False
            else:
                print('That was too short - please enter a minimum of 3 characters')
    return s_artist_nm


def artist_tabulate(po_results):
    """
        Generate a list of artist data in a tabular format
    :param po_results: Results object containing artist data
    :return: tabular list
    """
    l_artists = [[idx + 1, d_artist['name'], d_artist['type'], d_artist['country'], d_artist['score'], ','.join(d_artist['tags'][0:5])] for idx, d_artist in enumerate(po_results.l_result)]
    s_tab = tabulate(l_artists, headers=['Number', 'Artist Name', 'Artist Type', 'Country', 'Score', 'Tags'], tablefmt='orgtbl')
    return s_tab


def select_artist(ps_artist_tab, po_results):
    """
        CLI script to prompt user to select item from list
    :param ps_artist_tab: tabular list
    :param po_results: Results object containing artist data
    :return: integer representing user's choice of artist
    """
    print()
    print(ps_artist_tab)
    print()
    print(f"Above are the {str(Config.max_artists_to_list)} highest ranked results")
    print("Please enter the number of the artist you wish to search, or enter 0 to start over.")
    i_selection = None
    while not i_selection and i_selection != 0:
        try:
            i_selection = int(input("Artist Number: "))
            if i_selection < 0 or i_selection > len(po_results.l_result):
                raise ValueError
        except ValueError:
            i_selection = None
            print("Invalid selection, please re-enter")
    return i_selection


def handle_error(ps_search_type, po_result):
    """
        Basic error reporting
    :param ps_search_type: the item that was searched for - i.e. artist, song or lyric
    :param po_result: Results object containing error details
    """
    print(f"Sorry, the following error was encountered whilst searching for {ps_search_type}. Please try again later.")
    print(po_result.s_error_message)
    exit(-1)


def bar_chart(po_lyrics, pl_word_counts, ps_artist):
    """
       Uses numpy/matplotlib to display a bar chart on the user's desktop. Works okay in Win 10 :-)
    :param po_lyrics: Results object containing lyrics data
    :param pl_word_counts: list of word count - synchronised with po_lyrics
    :param ps_artist: artist name
    """
    l_songs = [lyr['song_title'] for lyr in po_lyrics.l_result]
    y_pos = np.arange(len(l_songs))
    plt.barh(y_pos, pl_word_counts, align='center', alpha=0.5)
    plt.yticks(y_pos, l_songs)
    plt.xlabel('Word Count')
    plt.title(f"Words per song for {ps_artist}")

    plt.show()


def present_results(ps_artist, po_lyrics):
    """
        CLI script to present results to user, and optionally display chart(s)
    :param ps_artist: artist name
    :param po_lyrics: Results object containing lyrics data
    """
    l_word_totals = word_count.lyrics_totals(po_lyrics=po_lyrics)
    i_average_words = word_count.average_words(pl_word_counts=l_word_totals)
    print()
    print(f"The average number of words in a {ps_artist} song is {str(i_average_words)}")
    i_min, i_max = word_count.min_max(pl_word_counts=l_word_totals)
    l_min_idx, l_max_idx = word_count.min_max_idx(pl_word_counts=l_word_totals, pi_min=i_min, pi_max=i_max)
    print(f"The song(s) with the fewest words ({str(i_min)}):  {','.join([po_lyrics.l_result[idx]['song_title'] for idx in l_min_idx])}")
    print(f"The song(s) with the most words ({str(i_max)}): {','.join([po_lyrics.l_result[idx]['song_title'] for idx in l_max_idx])}")
    s_show_bar = input("Would you like to see a bar chart (Y/N)?")
    if s_show_bar.upper() == 'Y':
        bar_chart(po_lyrics=po_lyrics, pl_word_counts=l_word_totals, ps_artist=ps_artist)


# if __name__ == "__main__":
def run_cli():
    i_selected_artist = 0
    o_artist_results = None

    while i_selected_artist >= 0:
        s_artist_name = request_artist_name()
        o_artist_results = artists.search_artists(ps_artist_name=s_artist_name)
        if o_artist_results.b_error:
            handle_error(ps_search_type='artists', po_result=o_artist_results)
        i_selected_artist = select_artist(ps_artist_tab=artist_tabulate(po_results=o_artist_results), po_results=o_artist_results)

        while i_selected_artist > 0:
            i_idx = i_selected_artist - 1
            s_artist = o_artist_results.l_result[i_idx]['name']
            print(f"You have chosen {s_artist}. Retrieving songs...")
            o_songs_results = songs.song_list(ps_artist_id=o_artist_results.l_result[i_idx]['id'])
            if o_songs_results.b_error:
                handle_error(ps_search_type='songs', po_result=o_artist_results)
            if len(o_songs_results.l_result) < 1:
                print(f"Sorry, there are no songs in the database for {s_artist}")
                i_selected_artist = 0
            else:
                print(f"There are {str(len(o_songs_results.l_result))} songs attributed to {s_artist}. Retrieving lyrics...")
            if i_selected_artist >= 0:
                o_lyrics_results = lyrics.retrieve_lyrics(ps_artist=s_artist, po_songs=o_songs_results)
                if o_lyrics_results.b_error:
                    handle_error(ps_search_type='lyrics', po_result=o_lyrics_results)
                if len(o_lyrics_results.l_result) < 1:
                    print(f"Sorry, no lyrics were found for {s_artist}")
                else:
                    print(f"Lyrics were retrieved for {str(len(o_lyrics_results.l_result))} songs.")
                    present_results(ps_artist=s_artist, po_lyrics=o_lyrics_results)
                i_selected_artist = 0
