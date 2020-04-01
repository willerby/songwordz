import re
import string


def clean_text(ps_lyrics):
    """
        Removes punctuation and various strings from lyrics
    :param ps_lyrics: a string containing a song's lyrics
    :return: a list of words
    """
    # remove verse / chorus text
    s_lyrics = re.sub(r'\[verse [0-9]*\]', "", ps_lyrics, flags=re.IGNORECASE)
    s_lyrics = re.sub(r'\[chorus\]', "", s_lyrics, flags=re.IGNORECASE)
    l_words = s_lyrics.split()
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    l_words = [w.translate(table) for w in l_words]
    return l_words


def word_count(ps_lyrics):
    """
       Counts the number of words in a song
    :param ps_lyrics:  a string containing a song's lyrics
    :return: an integer representing total words  in a song
    """
    # clean up the text
    l_lyrics = clean_text(ps_lyrics=ps_lyrics)

    return len(l_lyrics)


def lyrics_totals(po_lyrics):
    """
        Processes the lyrics results, counting the
    :param po_lyrics: Results object containing a list of artist lyrics
    :return: list of integers, representing total words in each song. synchronised to Results object
    """
    l_word_counts = [word_count(ps_lyrics=lyr['lyrics']) for lyr in po_lyrics.l_result]
    return l_word_counts


def average_words(pl_word_counts):
    """
        Returns the average number of word for a collection of songs
    :param pl_word_counts: list of integers
    :return: average (rounded)
    """
    try:
        i_average_words = round(sum(pl_word_counts) / len(pl_word_counts))
    except ZeroDivisionError:  # shouldn't happen, but...
        i_average_words = 0
    return i_average_words


def min_max(pl_word_counts):
    """
        Returns the lowest and highest values in a list of integers
    :param pl_word_counts: list of integers
    :return: minimum and maximum values from a list of integers
    """
    i_min, i_max = min(pl_word_counts), max(pl_word_counts)
    return i_min, i_max


def min_max_idx(pl_word_counts, pi_min, pi_max):
    """
        Returns two lists of list indices for minimum and maximum values in a list
    :param pl_word_counts: list of integers
    :param pi_min: min value
    :param pi_max: max values
    :return: two lists of list indices
    """
    l_min_idx = [i for i, e in enumerate(pl_word_counts) if e == pi_min]
    l_max_idx = [i for i, e in enumerate(pl_word_counts) if e == pi_max]
    return l_min_idx, l_max_idx
