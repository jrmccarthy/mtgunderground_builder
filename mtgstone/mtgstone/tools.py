from __future__ import absolute_import, print_function

"""
This is where I store various conversion tools, as there's a lot of conversions
since this app doesnt have a database and relies heavily on b64 encodings
of current user data
"""

def encoded_deck_info_to_deck_info(encoded_blob):
	"""
	Given a b64 encoded deck_info blob, return a string of if
	"""
	# TODO: Actually do this
	try:
		return "{}"
	except:
		return "{}"


def deck_info_to_dict(deck_info):
	"""
	Given a deck_info blob (a string)
	"""
	return {}

def encoded_to_dict(encoded_blob):
	"""Get and encoded blob, return a nice python dict of deck_info"""
	# TODO: This probably needs some error checking?
	return deck_info_to_dict(ncoded_deck_info_to_deck_info(encoded_blob))