from __future__ import print_function

import random

from rest_framework.views import APIView
from rest_framework.response import Response
import consts
import tools


class IndexView(APIView):
    """
    Basic welcome page I guess? Not much here yet
    """

    def get(self, request, format=None):
        return Response({"hi": "hi"})


class DeckView(APIView):
    """
    Take in the associated deck encoded blob and render the deck page
    """
    def get(self, request, deck_blob, format=None):
        # TODO: All of this!
        return Response({"hi": "hi", "blob": deck_blob})


class BuilderView(APIView):
    """
    All the magic happens here.

    This thing is where we do the real work. It takes in and existing deck-in-progress,
    figures out the next question, and presents it. Ideally this will always present
    the same options for the same RNGSeed, but it might not for a while.
    """
    def post(self, request, deck_blob, format=None):
        # TODO: All of this!
        # TODO: Figure out the card_choice from the POST
        card_choice = ""
        return Response({"hi": "hi", "blob": deck_blob, "choice": card_choice})

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