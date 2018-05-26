from __future__ import print_function
import consts
import requests
import random

"""
This is where I store various conversion tools, as there's a lot of conversions
since this app doesnt have a database and relies heavily on b64 encodings
of current user data
"""

###################
# Tools for dealing with the deck data blob that gets passed back and forth on requests
###################

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

#################
# Tools for dealing with scryfall / whatever we use to source cards
#################

def scryfall_query_builder(deck_colors, query_type, deck_format):
    """
    Build the query argument that we're gonna send to Scryfall to get our list of cards.
    """
    base_query = consts.BASE_QUERIES[deck_format]
    color_query = consts.COLOR_QUERIES[deck_colors]
    query_params = consts.QUERIES[deck_format][query_type]['query'] % {'colors': color_query}

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

def trim_query_result(query_result):
    """
    Scryfall returns an insane amount of data about each card. Frankly, we don't care about 98% of it. Trim this down
    to the stuff that really matters
    """
    good_stuff = ['id', 'oracle_id', 'name', 'cmc', 'colors', 'set', 'usd', 'image_uris']

    # UGHHHH I hate this, but I don't feel like refactoring into map or comprehensions right now.
    final = []
    for card in query_result['data']:
        card_dict = {}
        for k, v in card.items():
            if k in good_stuff:
                card_dict[k] = v
        final.append(card_dict)

    return final


####################
# Tools to select which card class to query and pick
####################

def collect_queries_by_weight(deck_format):
    """
    Based on weights, generate a list of queries to randomly choose from.
    """
    result = []
    for query_name, details in consts.QUERIES[deck_format].items():
        this_query = [query_name] * details.get('weight', 0)
        result += this_query

    return result

def pick_next_card_query(deck_format):
    """
    Pick a random query to use for the next card choice
    """
    return random.choice(collect_queries_by_weight(deck_format))