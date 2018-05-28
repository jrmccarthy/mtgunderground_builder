from __future__ import print_function


"""
Test out the various schemas, and make sure they match the actual data we are using.
"""
import jsonschema
import pytest

import mtgstone.consts as consts

def test_test():
    assert 1+1 == 2

class TestDeckSchema(object):
    """
    Tests related to the Deck schema
    """
    def test_empty_deck(self):
        empty = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[]}
        jsonschema.validate(empty, consts.DECK_SCHEMA)

    def test_deck_with_cards(self):
        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 1, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
            {'name': 'Swords to Plowshares', 'quantity': 2, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
            {'name': 'Purelace', 'quantity': 3, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
            {'name': 'Serra Angel', 'quantity': 4, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        jsonschema.validate(deck, consts.DECK_SCHEMA)

    def test_bad_color(self):
        # Not a color
        deck = {'format': 'Old School 93-94', 'colors': 'p', 'cards':[]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        # 3 colors not supported
        deck = {'format': 'Old School 93-94', 'colors': 'wub', 'cards':[]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        # 5 def not OK
        deck = {'format': 'Old School 93-94', 'colors': 'wubrg', 'cards':[]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

    def test_bad_format(self):
        deck = {'format': 'A Fake Format', 'colors': 'w', 'cards':[]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

    def test_bad_quantity(self):
        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 5, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 0, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

    def test_missing_properties(self):
        deck = {'format': 'Old School 93-94', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 4, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        deck = {'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 4, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        deck = {'format': 'Old School 93-94', 'colors': 'w'}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'quantity': 4, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 4, 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 4, 'set': 'lea', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        # Note: THIS IS OK! USD is not required
        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 4, 'set': 'lea', 'png': 'https://example.com/png'},
        ]}
        jsonschema.validate(deck, consts.DECK_SCHEMA)

    def test_extra_properties(self):
        deck = {'format': 'Old School 93-94', 'colors': 'w', 'extrathing': 'bad', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 4, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 4, 'set': 'lea', 'png': 'https://example.com/png', 'extra_prop': 'bad', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

    def test_set_too_long(self):
        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 4, 'set': 'leazz', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

    # So I guess this is a fake format, or the python jsonschema library doesnt validate it anyway
    # def test_bad_uri(self):
    #     deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
    #         {'name': 'Benalish Hero', 'quantity': 4, 'set': 'lea', 'png': 'wtf', 'usd': 0.01},
    #     ]}
    #     with pytest.raises(jsonschema.exceptions.ValidationError):
    #         jsonschema.validate(deck, consts.DECK_SCHEMA)

    def test_bad_types(self):
        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': "4", 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        deck = {'format': 'Old School 93-94', 'colors': 2, 'cards':[
            {'name': 'Benalish Hero', 'quantity': 4, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)

        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':{}}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck, consts.DECK_SCHEMA)


class TestSelectionSchema(object):
    """
    Tests related to the Selection schema
    """
    def test_good_selection(self):
        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'max_can_add': 4, 'colors': ['W'],
        }
        jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        # Multicolor
        selection = {
            'name': 'Stangg', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 6,
            'max_can_add': 1, 'colors': ['R', 'G'],
        }
        jsonschema.validate(selection, consts.SELECTION_SCHEMA)

    def test_bad_colors(self):
        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'max_can_add': 4, 'colors': ['P'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'max_can_add': 4, 'colors': ['W', 'P'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

    def test_bad_cmc(self):
        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1.5,
            'max_can_add': 4, 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': '1',
            'max_can_add': 4, 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

    def test_bad_max_can_add(self):
        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'max_can_add': 5, 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'max_can_add': 0, 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

    def test_missing_properties(self):
        selection = {
            'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'max_can_add': 4, 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        selection = {
            'name': 'Benalish Hero', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'max_can_add': 4, 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'usd': 0.01, 'cmc': 1,
            'max_can_add': 4, 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'cmc': 1,
            'max_can_add': 4, 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        # We don't need to get back the cmc, max_can_add, or cmc, because we dont use them later
        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01,
            'max_can_add': 4, 'colors': ['W'],
        }
        jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'colors': ['W'],
        }
        jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'max_can_add': 4,
        }
        jsonschema.validate(selection, consts.SELECTION_SCHEMA)

    def test_extra_properties(self):
        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'max_can_add': 4, 'colors': ['W'], 'extra_thing': 'bad',
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

    def test_bad_types(self):
        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1,
            'max_can_add': '4', 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': 1.5,
            'max_can_add': 4, 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)

        selection = {
            'name': 'Benalish Hero', 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01, 'cmc': '1',
            'max_can_add': 4, 'colors': ['W'],
        }
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(selection, consts.SELECTION_SCHEMA)