from __future__ import print_function


"""
Test out all the stuff that creates and messes with decklists
"""
import copy
import jsonschema
import pytest

import mtgstone.consts as consts
import mtgstone.tools as tools


class TestDeckManipulation(object):

    def test_success_empty_deck(self):
        deck = {'format': 'Old School 93-94', 'colors':'w', 'cards': []}
        empty_deck = tools.gen_empty_deck(deck_format='Old School 93-94', colors='w')

        assert empty_deck == deck

    def test_empty_deck_fake_colors(self):
        with pytest.raises(tools.InvalidDeckDataException):
            empty_deck = tools.gen_empty_deck(deck_format='Old School 93-94', colors='p')

        with pytest.raises(tools.InvalidDeckDataException):
            empty_deck = tools.gen_empty_deck(deck_format='Old School 93-94', colors='pwe')

        with pytest.raises(tools.InvalidDeckDataException):
            empty_deck = tools.gen_empty_deck(deck_format='Old School 93-94', colors='wub')

    def test_empty_deck_fake_format(self):
        with pytest.raises(tools.InvalidDeckDataException):
            empty_deck = tools.gen_empty_deck(deck_format='Fake format', colors='w')

    def test_empty_deck_seeded(self):
        # TODO: Write this once rng seeding is implemented
        pass

    def test_success_add_card(self):
        deck = {'format': 'Old School 93-94', 'colors':'w', 'cards': []}
        card = {'name': 'Healing Salve', 'set': 'lea', 'usd': 0.01, 'png': 'https://example.com/salve', 'cmc': 1, 'colors': ['W']}
        updated_deck = {'format': 'Old School 93-94', 'colors':'w', 'cards': [
            {'name': 'Healing Salve', 'quantity': 4, 'set': 'lea', 'png': 'https://example.com/salve', 'usd': 0.01}
        ]}

        new_deck = tools.add_card_to_deck(deck, card, quantity=4)
        assert new_deck == updated_deck


    def test_add_card_bad_card(self):
        deck = {'format': 'Old School 93-94', 'colors':'w', 'cards': []}
        card = {'name': 'Healing Salve', 'usd': 0.01, 'png': 'https://example.com/salve', 'cmc': 1, 'colors': ['W']}

        with pytest.raises(tools.InvalidCardDateException):
            new_deck = tools.add_card_to_deck(deck, card, quantity=4)

    def test_add_card_bad_existing_deck(self):
        deck = {'format': 'Old School 93-94', 'colors':'p', 'cards': []}
        card = {'name': 'Healing Salve', 'set': 'lea', 'usd': 0.01, 'png': 'https://example.com/salve', 'cmc': 1, 'colors': ['W']}

        with pytest.raises(tools.InvalidDeckDataException):
            new_deck = tools.add_card_to_deck(deck, card, quantity=4)

    def test_add_card_success_high_quant(self):
        deck = {'format': 'Old School 93-94', 'colors':'w', 'cards': []}
        card = {'name': 'Healing Salve', 'set': 'lea', 'usd': 0.01, 'png': 'https://example.com/salve', 'cmc': 1, 'colors': ['W']}
        updated_deck = {'format': 'Old School 93-94', 'colors':'w', 'cards': [
            {'name': 'Healing Salve', 'quantity': 12, 'set': 'lea', 'png': 'https://example.com/salve', 'usd': 0.01}
        ]}

        new_deck = tools.add_card_to_deck(deck, card, quantity=12, validate=False)
        assert new_deck == updated_deck

    def test_add_card_failed_high_quant(self):
        deck = {'format': 'Old School 93-94', 'colors':'w', 'cards': []}
        card = {'name': 'Healing Salve', 'set': 'lea', 'usd': 0.01, 'png': 'https://example.com/salve', 'cmc': 1, 'colors': ['W']}

        with pytest.raises(tools.InvalidDeckDataException):
            new_deck = tools.add_card_to_deck(deck, card, quantity=12, validate=True)


class TestAddLands(object):
    """
    Separate grouping of all our land-related stuff
    """

    def test_success_add_lands(self):
        # Basic setup
        deck = {'format': 'Old School 93-94', 'colors': 'w', 'cards': []}
        quantity = 24
        expected = {'format': 'Old School 93-94', 'colors': 'w', 'cards': [
            {
                'name': consts.STATIC_LAND_SELECTIONS['w']['name'],
                'set': consts.STATIC_LAND_SELECTIONS['w']['set'],
                'usd': consts.STATIC_LAND_SELECTIONS['w']['usd'],
                'png': consts.STATIC_LAND_SELECTIONS['w']['png'],
                'quantity': quantity,
                'usd': consts.STATIC_LAND_SELECTIONS['w']['usd'],
            }
        ]}

        # Higher number of lands
        new_deck = tools.add_lands(deck)
        assert new_deck == expected

        higher_quant = tools.add_lands(deck, lands_needed=40)
        update_expected = copy.deepcopy(expected)
        update_expected['cards'][0]['quantity'] = 40

        assert higher_quant == update_expected

        # 2 colors (all combos ideally)
        pass

    def test_add_lands_bad_colors(self):
        pass
