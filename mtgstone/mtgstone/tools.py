from __future__ import absolute_import, print_function
import consts
import requests

"""
This is where I store various conversion tools, as there's a lot of conversions
since this app doesnt have a database and relies heavily on b64 encodings
of current user data
"""

def encoded_deck_info_to_deck_info(encoded_blob):
    """
    Given a b64 encoded deck_info blob, return a string of it
    """
    # TODO: Actually do this
    try:
        return "{}"
    except:
        return "{}"


def deck_info_to_dict(deck_info):
    """
    Given a deck_info blob (a string), decode it into a dictionary
    """
    return {}

def encoded_to_dict(encoded_blob):
    """Get an encoded blob, return a nice python dict of deck_info"""
    # TODO: This probably needs some error checking?
    return deck_info_to_dict(ncoded_deck_info_to_deck_info(encoded_blob))

def scryfall_query_builder(deck_colors, query_type, deck_format):
    """
    Build the query argument that we're gonna send to Scryfall to get our list of cards.
    """
    base_query = consts.BASE_QUERIES[deck_format]
    color_mixin = consts.COLOR_MIXINS[deck_colors]
    query_params = consts.QUERIES[deck_format][query_type]['query'] % {'colors': color_mixin}

    full_query = ' '.join([base_query, query_params])

    return full_query

def get_cards(query_param):
    """
    Someday if I add caching of queries, this is the method that will populate/check the cache.
    For now, it just passes through the query.

    If anyone actually uses this, adding caching should be really simple; just need a place to store the data.
    Scryfall doesnt really want unauthed accounts blasting their API (for good reason).
    """
    return query_scryfall(query_param)

def query_scryfall(query_param):
    """
    Reach out to scryfall and get our card data.
    """
    params = 'q=%s' % query_param
    result = requests.get(consts.QUERY_URL, params)
    try:
        result.raise_for_status()
    except Exception as e:
        print('Bad stuff: ')
        print(result.content)
        raise

    return result.json()

