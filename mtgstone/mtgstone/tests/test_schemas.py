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
        deck_ = {'format': 'Old School 93-94', 'colors': 'wub', 'cards':[]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck_, consts.DECK_SCHEMA)

        # 5 def not OK
        deck__ = {'format': 'Old School 93-94', 'colors': 'wubrg', 'cards':[]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck__, consts.DECK_SCHEMA)

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

        deck_ = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 0, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(deck_, consts.DECK_SCHEMA)

    def test_missing_properties(self):
        pass

    def test_extra_properties(self):
        pass

    def test_set_too_long(self):
        pass

    def test_bad_uri(self):
        pass