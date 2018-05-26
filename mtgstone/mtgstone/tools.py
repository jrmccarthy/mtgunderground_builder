from __future__ import print_function
import requests
import random
import json
import jsonschema

import consts
import deck_formatting

"""
This is where I store various conversion tools, as there's a lot of conversions
since this app doesnt have a database and relies heavily on b64 encodings
of current user data
"""

###################
# Tools for dealing with the deck data blob that gets passed back and forth on requests
###################

class InvalidDeckDataException(Exception):
    # Just a custom error for ease of use
    pass


def encoded_string_to_string(encoded_blob):
    """
    Given a b64 encoded deck_info blob, return a string of it
    """
    try:
        return encoded_blob.decode("base64")
    except Exception:
        raise InvalidDeckDataException("Cannot decode deck data into anything readable.")

def string_to_usable_deck(deck_string):
    """
    Given a deck_string blob (a string), decode it into a dictionary
    """
    try:
        result = json.loads(deck_string)
    except Exception:
        raise InvalidDeckDataException("Deck data does not appear to be valid JSON")

    try:
        jsonschema.validate(result, deck_formatting.DECK_SCHEMA)
    except Exception as e:
        # For now, reraise the original error, because it was useful and important context
        raise
        # raise InvalidDeckDataException(e.message)

    return result

def encoded_string_to_usable_deck(encoded_blob):
    """Get an encoded blob, return a nice python dict of deck_info"""
    return deck_info_to_dict(encoded_deck_info_to_deck_info(encoded_blob))

def usable_deck_to_string(usable_deck):
    """Take a nice Python Dict formatted deck and turn it into a string
    """
    jsonschema.validate(usable_deck, deck_formatting.DECK_SCHEMA)
    return json.dumps(usable_deck)

def string_to_encoded_string(deck_string):
    """
    Take a string that hopefully is a json-dumped version of a usable deck and encode it
    """
    return deck_string.encode("base64")

def usable_deck_to_encoded_string(usable_deck):
    """Go from a usable Deck dict all the way to an encoded string"""
    return string_to_encoded_string(usable_deck_to_string(usable_deck))

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

    Return the list sorted at the end so that its always in the same order for a format.
    """
    result = []
    for query_name, details in consts.QUERIES[deck_format].iteritems():
        this_query = [query_name] * details.get('weight', 0)
        result += this_query

    return sorted(result)

def pick_next_card_query(deck_format, seed=None):
    """
    Pick a random query to use for the next card choice
    """
    return random.choice(collect_queries_by_weight(deck_format))

##################
# Tools for actually manipulating the deck blob
##################

def gen_empty_deck(deck_format, colors, seed=None):
    empty_deck = {
        "colors": colors,
        "deck_format": deck_format,
        "cards": [],
    }
    if seed:
        empty_deck['seed'] = seed
    jsonschema.validate(empty_deck, deck_formatting.DECK_SCHEMA)
    
    return empty_deck

def add_card_to_deck(deck, card_info, quantity):
    pass
