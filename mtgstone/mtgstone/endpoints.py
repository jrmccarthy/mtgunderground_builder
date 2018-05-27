from __future__ import print_function

import json
import random
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

import consts
import tools

# TODO: Make this configurable at deck creation
MAX_DECK_SIZE = 36 # Add 24 lands by default!


class IndexView(APIView):
    """
    Basic info about the app. List the options available to the user, necessary for deck creation.
    """

    def get(self, request, format=None):
        return Response({'available_formats': [item for item in consts.FORMATS], 'available_colors': [item for item in consts.COLOR_QUERIES]})


class DeckView(APIView):
    """
    Take in the associated deck encoded blob and render the deck page
    """
    def get(self, request, deck_blob=None, format=None):
        """
        Lets make finished decks shareable! Also for the frontend to easily to its thing. This
        endpoint will simple decode a deck_blob and return the decoded stuff, for someone else
        to handle displaying at some future date.
        """
        if deck_blob:
            try:
                result = tools.encoded_string_to_usable_deck(deck_blob)
            except tools.InvalidDeckDataException as e:
                raise APIException(e.message)
        else:
            # TODO: what do do here?
            result = ''
        return Response({"deck": result})

    def post(self, request, format=None):
        """
        This endpoint lets you start a new deckbuilding experience! Include, in your post data,
        what color(s) you want, and your desired format. We'll return a JSON response with an ID
        for your current deck, and a json blob describing your available card choices.
        """
        # Grab the info we need from the post data; if not JSON or not there, error
        post_data = request.data
        if 'colors' not in post_data or 'format' not in post_data:
            raise APIException('Must include both "colors" and "format" in POST data')

        # Generate an empty deck (tools) with the chosen data. Error if its crap etc.
        new_deck = tools.gen_empty_deck(post_data['format'], post_data['colors'])
        deck_blob = tools.usable_deck_to_encoded_string(new_deck)

        # Figure out the next query, run it, and pick a set of cards for the user to select from
        next_selection = tools.next_card_selection(new_deck)

        # Collect up all that data and return it to the user for their perusal.
        return Response({
            'deck_blob': deck_blob, 
            'next_selection': next_selection, 
            'complete': False,
            'post_to': '/builder/',
            'debug': {'deck': new_deck},
        })


class BuilderView(APIView):
    """
    All the magic happens here.

    This thing is where we do the real work. It takes in and existing deck-in-progress,
    figures out the next question, and presents it. Ideally this will always present
    the same options for the same RNGSeed, but it might not for a while.
    """
    def post(self, request, format=None):
        """
        This endpoint handles the actual deckbuilding stuff. It validates the posted deck blob,
        validates the posted card choice, then adds the card to the deck and updates the blob.
        Then it figures out if the deck is done (based on number of cards), and adds lands if so.

        If its done, it returns that info to the front end to handle. If not, it returns an updated
        deck blob along with a new card choice, and the whole process repeats.
        """
        post_data = request.data
        if 'deck_blob' not in post_data or 'next_selection' not in post_data or 'quantity' not in post_data:
            raise APIException('Must include "deck_blob", "next_selection", and "quantity" in POST data')
        
        # Validate the existing deck blob
        deck_data = tools.encoded_string_to_usable_deck(post_data['deck_blob'])

        # Validate the selection
        selection = post_data['next_selection']
        tools.validate_selection(selection)

        # Add the selection to the deck
        new_deck = tools.add_card_to_deck(deck_data, selection, post_data['quantity'])
        
        # Figure out if we are done (count how many total cards in deck)
        # TODO: This part
        deck_count = tools.count_deck(new_deck)
        if deck_count >= MAX_DECK_SIZE:
            # Add lands (super basic for now)
            finished_deck = tools.add_lands(new_deck)
            deck_blob = tools.usable_deck_to_encoded_string(finished_deck)

            return Response({
                    'deck_blob': deck_blob, 
                    'complete': True,
                    'debug': {'deck': finished_deck},
                })

        # print('\nCount: %s\n' % deck_count)

        # If so, return info indicating we are done!
        # TODO: This too
        
        # Else, grab the next selection and return
        deck_blob = tools.usable_deck_to_encoded_string(new_deck)
        next_selection = tools.next_card_selection(new_deck)

        return Response({
            'deck_blob': deck_blob, 
            'next_selection': next_selection, 
            'complete': False,
            'post_to': '/builder/',
            'debug': {'deck': new_deck},
        })

class QueryTestView(APIView):
    """
    Just an endpoint for testing out the query builder. Grab a random format/category/color, build
    a query, and return the results.
    """
    def get(self, request, format=None):
        format_ = random.choice(consts.FORMATS)
        color = random.choice(consts.COLOR_QUERIES.items())[0]
        chosen_query = random.choice(consts.QUERIES[format_].items())[0]

        final_query = tools.scryfall_query_builder(color, chosen_query, format_)
        query_result = tools.trim_query_result(tools.query_scryfall(final_query))

        return Response({'format': format_, 'num': len(query_result), 'color': color, 
            'chosen_query': chosen_query, 'query_result': query_result})