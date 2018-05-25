from __future__ import absolute_import, print_function

from rest_framework.views import APIView
from rest_framework.response import Response


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