from __future__ import absolute_import, print_function

"""
This file holds all the various consts. Since we don't have a database, we
need to keep static data here, like what formats we support, what queries
to use for various things on scryfall, 
"""

FORMATS = [
	"Old School 93-94",
]

RESTRICTIONS = {
	"Old School 93-94": [
		"Black Lotus",
		"Mox Sapphire", # TODO: Add more! 
	],
}

QUERIES = {
	"Old School 93-94": {
		"Creatures": "", # TODO: Add more
	}
}

