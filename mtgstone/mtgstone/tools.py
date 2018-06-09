from __future__ import print_function

import copy
import json
import jsonschema
import math
import random
import requests

import consts

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


class InvalidCardDateException(Exception):
    pass


def _encoded_string_to_string(encoded_blob):
    """
    Given a b64 encoded deck_info blob, return a string of it
    """
    try:
        return encoded_blob.decode("base64")
    except Exception:
        raise InvalidDeckDataException("Cannot decode deck data into anything readable.")

def _string_to_usable_deck(deck_string):
    """Given a deck_string blob (a string), decode it into a dictionary"""
    try:
        result = json.loads(deck_string)
    except Exception:
        raise InvalidDeckDataException("Deck data does not appear to be valid JSON")

    try:
        jsonschema.validate(result, consts.DECK_SCHEMA)
    except Exception as e:
        # For now, reraise the original error, because it is useful and has important context
        raise
        # raise InvalidDeckDataException(e.message)

    return result

def encoded_string_to_usable_deck(encoded_blob):
    """Get an encoded blob, return a nice python dict of deck_info"""
    return _string_to_usable_deck(_encoded_string_to_string(encoded_blob))

def _usable_deck_to_string(usable_deck):
    """Take a nice Python Dict formatted deck and turn it into a string"""
    # TODO: Right now the validator doesnt work once you add >4 of a basic; once thats fixed
    # this can be enabled again
    # jsonschema.validate(usable_deck, consts.DECK_SCHEMA)
    return json.dumps(usable_deck)

def _string_to_encoded_string(deck_string):
    """Take a string that hopefully is a json-dumped version of a usable deck and encode it"""
    return deck_string.encode("base64")

def usable_deck_to_encoded_string(usable_deck):
    """Go from a usable Deck dict all the way to an encoded string"""
    return _string_to_encoded_string(_usable_deck_to_string(usable_deck))

#################
# Tools for dealing with scryfall / whatever we use to source cards
#################

def _scryfall_query_builder(colors, query_type, deck_format):
    """
    Build the query argument that we're gonna send to Scryfall to get our list of cards.
    """
    base_query = consts.BASE_QUERIES[deck_format]
    color_query = consts.COLOR_QUERIES[colors]
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
    return _query_scryfall(query_param)

def _query_scryfall(query_param):
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

def _trim_query_result(query_result):
    """
    Scryfall returns an insane amount of data about each card. Frankly, we don't care about 98% of it. Trim this down
    to the stuff that really matters
    """
    good_stuff = ['name', 'cmc', 'colors', 'set', 'usd']

    # UGHHHH I hate this, but I don't feel like refactoring into map or comprehensions right now.
    final = []
    for card in query_result['data']:
        card_dict = {}
        for k, v in card.items():
            if k in good_stuff:
                card_dict[k] = v
        card_dict['png'] = card['image_uris'].get('png')
        if not card['image_uris'].get('png'):
            raise IndexError('WTF: ', card['image_uris'], card['name'])
        final.append(card_dict)

    return final

def compile_execute_and_trim_query(colors, query_type, deck_format):
    """
    Tie all the above together into an easier-to-use api
    """
    full_query = _scryfall_query_builder(colors, query_type, deck_format)
    cards = get_cards(full_query)
    return _trim_query_result(cards)


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
# Tools for generating a set of options for the user to pick from (e.g. the 3 cards they see)
##################

def generate_pickable_selections(trimmed_query_results, deck_format, current_deck, num_selections=3):
    """
    We probably have a big blob of JSON stuff here. Lets pick num_selections random items from
    it, but we need to be careful not to allow banned cards.

    # TODO: We should also deal with restricted cards, e.g. not present them for choice if they
    are already in the deck...
    """
    # Lets shuffle the results first, so we only have to randomize once
    random.shuffle(trimmed_query_results)
    result = []
    for item in trimmed_query_results:
        if not check_banned(deck_format, item['name']):
            if not check_restricted_allowed_in_deck(deck_format, current_deck, item['name']):
                # TODO: Calculate max_can_add based on current deck + restricted list
                item['max_can_add'] = 4
                result.append(item)
        # Once we have the right number of cards, we're done.
        if len(result) >= num_selections:
            break
    # If somehow there aren't enough cards... crap. For now, just grin and bear it. Someone
    # higher up the call stack can deal with this, maybe by asking for another query.
    return result

def check_banned(deck_format, card_name):
    """Check if the card_name is on the banned list for the format"""
    if card_name in consts.BANNINGS[deck_format]:
        return True
    return False

def check_restricted_allowed_in_deck(deck_format, current_deck, card_name):
    """
    This isnt implemented yet but it will check if the card_name is (restricted AND in the deck already).
    So that you don't end up with 2 sol rings for example.
    """
    # TODO: Do this
    return False

##################
# Tools for actually manipulating the deck blob
##################

def gen_empty_deck(deck_format, colors, seed=None):
    empty_deck = {
        "colors": colors,
        "format": deck_format,
        "cards": [],
    }
    print(empty_deck)
    if seed:
        empty_deck['seed'] = seed
    # jsonschema.validate(empty_deck, consts.DECK_SCHEMA)
    validate_deck(empty_deck)

    return empty_deck

def add_card_to_deck(deck, card_info, quantity, validate=True):
    """
    Add the chosen card to the deck, and return the updated blob. Validate the selection too.
    """
    if validate:
        validate_deck(deck)
    validate_selection(card_info)
    new_deck = copy.deepcopy(deck)
    # TODO: Figure out what to do about >4 of a card in a nice way.
    new_deck['cards'].append({
        "name": card_info['name'],
        "set": card_info['set'],
        "usd": card_info['usd'],
        "quantity": quantity,
        "png": card_info['png'],
    })

    if validate:
        validate_deck(new_deck)

    return new_deck

def add_lands(deck, lands_needed=24):
    """
    This is real simple for now. Add lands based on the deck color (24 total always for now).
    Some day this could get fancier, like taking ratios into mind, and maybe looking at lands
    already in the deck, but for now, just add basics (or 4 duals + 10 of each for 2colors).
    """
    deck_colors = deck['colors']
    if len(deck_colors) == 1:
        # mono color, this is easy
        final_deck = add_card_to_deck(deck, consts.STATIC_LAND_SELECTIONS[deck_colors], quantity=lands_needed, validate=False)
    elif len(deck_colors) == 2:
        with_duals = add_card_to_deck(deck, consts.STATIC_LAND_SELECTIONS[deck_colors], quantity=4)
        # Just put in half and half of each (or close nough, if we need an odd number of lands total)
        first_quant, second_quant = int(math.floor((lands_needed-4)/2.0)), int(math.ceil((lands_needed-4)/2.0))
        first_color = add_card_to_deck(with_duals, consts.STATIC_LAND_SELECTIONS[deck_colors[0]], first_quant, validate=False)
        final_deck = add_card_to_deck(first_color, consts.STATIC_LAND_SELECTIONS[deck_colors[1]], second_quant, validate=False)
    else:
        raise InvalidDeckDataException('Deck can only be one or two colors right now!')

    return final_deck

def next_card_selection(deck):
    """
    Given an existing deck, generate the next set of cards that should be presented to the user
    for selection.
    """
    # First grab the colors and format
    # Then generate the query, execute, and trim
    # Then get the selections, and return them!
    colors = deck['colors']
    deck_format = deck['format']
    seed = deck.get('seed')

    query_type = pick_next_card_query(deck_format, seed)
    trimmed_query_results = compile_execute_and_trim_query(colors, query_type, deck_format)
    selections = generate_pickable_selections(trimmed_query_results, deck_format, deck)
    print('QUERY: ', query_type, ' NUM RESULTS:', len(trimmed_query_results))

    return selections

def count_deck(deck):
    """Count how many cards in the deck (so we know when we're done)"""
    return reduce(lambda x, y: x + y['quantity'], deck['cards'], 0)

def validate_deck(deck, error='Deck does not appear to be valid'):
    try:
        jsonschema.validate(deck, consts.DECK_SCHEMA)
    except Exception:
        raise InvalidDeckDataException(error)

def validate_selection(selection):
    try:
        jsonschema.validate(selection, consts.SELECTION_SCHEMA)
    except Exception as e:
        raise InvalidCardDateException(e.message)
