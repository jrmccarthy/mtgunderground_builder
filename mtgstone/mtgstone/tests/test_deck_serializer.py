from __future__ import print_function

"""
Test out all the deck serialization junk
"""
import json
import jsonschema
import pytest
import mtgstone.tools as tools
import mtgstone.consts as consts

class TestDecklistEncoderAndDecoder(object):
    """
    These tests deal with taking a nice Python decklist object and turning it into a b64 encoded string,
    and everything along the way
    """
    ######## B64 -> Object stuff

    def test_success_b64_to_string(self):
        deck = json.dumps({'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 1, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
            {'name': 'Swords to Plowshares', 'quantity': 2, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]})
        good_deckstring = 'eyJjYXJkcyI6IFt7InVzZCI6IDAuMDEsICJzZXQiOiAibGVhIiwgIm5hbWUiOiAiQmVuYWxpc2gg\nSGVybyIsICJwbmciOiAiaHR0cHM6Ly9leGFtcGxlLmNvbS9wbmciLCAicXVhbnRpdHkiOiAxfSwg\neyJ1c2QiOiAwLjAxLCAic2V0IjogImxlYSIsICJuYW1lIjogIlN3b3JkcyB0byBQbG93c2hhcmVz\nIiwgInBuZyI6ICJodHRwczovL2V4YW1wbGUuY29tL3BuZyIsICJxdWFudGl0eSI6IDJ9XSwgImNv\nbG9ycyI6ICJ3IiwgImZvcm1hdCI6ICJPbGQgU2Nob29sIDkzLTk0In0=\n'

        result = tools._encoded_string_to_string(good_deckstring)

        assert result == deck

    def test_not_b64(self):
        bad_deckstring = 'asdf12345?<>'

        with pytest.raises(tools.InvalidDeckDataException):
            result = tools._encoded_string_to_string(bad_deckstring)

    def test_bad_format(self):
        """Note this should still pass, since this step doesnt validate anything but b64-ness"""
        deck = json.dumps({'format': 'bad', 'fake_thing': 'also_bad'})

        medium_deckstring = 'eyJmYWtlX3RoaW5nIjogImFsc29fYmFkIiwgImZvcm1hdCI6ICJiYWQifQ==\n'

        result = tools._encoded_string_to_string(medium_deckstring)

        assert result == deck

    def test_success_string_to_object(self):
        deck = '{"format": "Old School 93-94", "colors": "w", "cards": []}'

        result = tools._string_to_usable_deck(deck)

    def test_not_valid_json(self):
        deck = '{"format": "Old School 93-94", "colors": w, "cards": []}'

        with pytest.raises(tools.InvalidDeckDataException):
            result = tools._string_to_usable_deck(deck)

    def test_invalid_deck_format(self):
        deck = '{"format": "Not a real one", "colors": "w", "cards": []}'

        with pytest.raises(jsonschema.exceptions.ValidationError):
            result = tools._string_to_usable_deck(deck)

    ######### Object -> B64 stuff

    def test_success_object_to_string(self):
        """This test is kinda junk for now, sorry"""
        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 1, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
            {'name': 'Swords to Plowshares', 'quantity': 2, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]}

        result = tools._usable_deck_to_string(deck)

        assert result == json.dumps(deck)

    def test_bad_format(self):
        """Make sure invalid decklists dont sneak through"""
        # TODO: Once validation is reenabled on this method, write this test
        pass

    def test_success_string_to_b64(self):
        deck = json.dumps({'format': 'Old School 93-94', 'colors': 'w', 'cards':[
            {'name': 'Benalish Hero', 'quantity': 1, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
            {'name': 'Swords to Plowshares', 'quantity': 2, 'set': 'lea', 'png': 'https://example.com/png', 'usd': 0.01},
        ]})
        good_deckstring = 'eyJjYXJkcyI6IFt7InVzZCI6IDAuMDEsICJzZXQiOiAibGVhIiwgIm5hbWUiOiAiQmVuYWxpc2gg\nSGVybyIsICJwbmciOiAiaHR0cHM6Ly9leGFtcGxlLmNvbS9wbmciLCAicXVhbnRpdHkiOiAxfSwg\neyJ1c2QiOiAwLjAxLCAic2V0IjogImxlYSIsICJuYW1lIjogIlN3b3JkcyB0byBQbG93c2hhcmVz\nIiwgInBuZyI6ICJodHRwczovL2V4YW1wbGUuY29tL3BuZyIsICJxdWFudGl0eSI6IDJ9XSwgImNv\nbG9ycyI6ICJ3IiwgImZvcm1hdCI6ICJPbGQgU2Nob29sIDkzLTk0In0=\n'

        result = tools._string_to_encoded_string(deck)

        assert result == good_deckstring

    def test_bad_format(self):
        """Note this should succeed, since this thing doesnt validiate at all, just transforms"""
        deck = json.dumps({'format': 'fake', 'colors': 'also fake'})
        good_deckstring = 'eyJjb2xvcnMiOiAiYWxzbyBmYWtlIiwgImZvcm1hdCI6ICJmYWtlIn0=\n'

        result = tools._string_to_encoded_string(deck)

        assert result == good_deckstring
