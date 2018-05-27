from __future__ import print_function

"""
This file holds all the various consts. Since we don't have a database, we
need to keep static data here, like what formats we support, what queries
to use for various things on scryfall,
"""

QUERY_URL = 'https://api.scryfall.com/cards/search'

FORMATS = [
    "Old School 93-94",
]

RESTRICTIONS = {
    "Old School 93-94": [
        "Ancestral Recall",
        "Balance",
        "Black Lotus",
        "Braingeyser",
        "Chaos Orb",
        "Channel",
        "Demonic Tutor",
        "Library of Alexandria",
        "Mana Drain",
        "Maze of Ith",
        "Mind Twist",
        "Mox Emerald",
        "Mox Jet",
        "Mox Pearl",
        "Mox Ruby",
        "Mox Sapphire",
        "Recall",
        "Regrowth",
        "Sol Ring",
        "Time Vault",
        "Time Walk",
        "Timetwister",
        "Wheel of Fortune",
    ],
}

BANNINGS = {
    "Old School 93-94": [
        "Bronze Tablet",
        "Contract from Below",
        "Darkpact",
        "Demonic Attorney",
        "Jeweled Bird",
        "Rebirth",
        "Tempest Efreet",
    ]
}

BASE_QUERIES = {
    "Old School 93-94": "year<=1994 unique:cards not:reprint",
}

COLOR_QUERIES = {
    "w": "c=w",
    "u": "c=u",
    "b": "c=b",
    "r": "c=r",
    "g": "c=g",
    "wu": "(c=w or c=u or c=wu)",
    "wb": "(c=w or c=b or c=wb)",
    "wr": "(c=w or c=r or c=wr)",
    "wg": "(c=w or c=g or c=wg)",
    "ub": "(c=u or c=b or c=ub)",
    "ur": "(c=u or c=r or c=ur)",
    "ug": "(c=u or c=g or c=ug)",
    "br": "(c=b or c=r or c=br)",
    "bg": "(c=b or c=g or c=bg)",
    "rg": "(c=r or c=g or c=rg)",
}

# This is all the magic queries we make to Scryfall to get lists of cards.
# The query is pretty obvious; colors gets filled in right before we execute.
# The weight parameter lets us make it so certain categories come up more (e.g. more creatures)
# For now, all the weights are 1; tuning this will probably suck a lot, but whatever.
QUERIES = {
    "Old School 93-94": {
        "1 or 2 Cost Creatures": {"query":"t:creature (cmc=1 or cmc=2) (%(colors)s or c=c)", "weight": 5},
        "3 Cost Creatures": {"query":"t:creature cmc=3 (%(colors)s or c=c)", "weight": 5},
        "4 Cost Creatures": {"query":"t:creature cmc=4 (%(colors)s or c=c)", "weight": 4},
        "5 Cost Creatures": {"query":"t:creature cmc=5 (%(colors)s or c=c)", "weight": 3},
        "6+ Cost Creatures": {"query":"t:creature cmc>=6 (%(colors)s or c=c)", "weight": 1},
        "Auras": {"query":"t:aura (%(colors)s or c=c)", "weight": 1},
        "Enchantments": {"query":"t:enchantment (%(colors)s or c=c)", "weight": 1},
        "Artifacts": {"query":"t:artifact -t:creature", "weight": 2},
        "Sorceries": {"query":"t:sorcery (%(colors)s or c=c)", "weight": 2},
        "Instants": {"query":"t:instant (%(colors)s or c=c)", "weight": 2},
        "Nonbasic Lands": {"query":"t:land -t:basic not:dual", "weight": 2},
        # TODO: Clean this up to only provide mana of the correct colors (from lands); all colors ok from spells.
        "Mana Acceleration": {"query":"(t:land -t:basic o:/add {(W|U|B|R|G|C)}{(W|U|B|R|G|C)}/) or \
            (-t:land o:/add {(W|U|B|R|G|C)}/ (%(colors)s or c=c))", "weight": 2},
        "Legends": {"query":"t:legend (%(colors)s or c=c)", "weight": 0},
        # "Removal": "", # Not sure how to query this one yet.
    }
}


STATIC_LAND_SELECTIONS = {
    "w": {
        "name": "Plains",
        "usd": "0.01",
        "cmc": 0,
        "colors": [],
        "set": "lea",
        "png": "https://img.scryfall.com/cards/png/en/lea/286.png?1525123704",
    },
    "u": {
        "name": "Island",
        "usd": "0.01",
        "cmc": 0,
        "colors": [],
        "set": "lea",
        "png": "https://img.scryfall.com/cards/png/en/lea/288.png?1525123442",
    },
    "b": {
        "name": "Swamp",
        "usd": "0.01",
        "cmc": 0,
        "colors": [],
        "set": "lea",
        "png": "https://img.scryfall.com/cards/png/en/lea/290.png?1525124024",
    },
    "r": {
        "name": "Mountain",
        "usd": "0.01",
        "cmc": 0,
        "colors": [],
        "set": "lea",
        "png": "https://img.scryfall.com/cards/png/en/lea/292.png?1525123589",
    },
    "g": {
        "name": "Forest",
        "usd": "0.01",
        "cmc": 0,
        "colors": [],
        "set": "lea",
        "png": "https://img.scryfall.com/cards/png/en/lea/294.png?1525123083",
    },
    "wu": {

    },
    "wb": {

    },
    "wr": {

    },
    "wg": {

    },
    "ub": {

    },
    "ur": {

    },
    "ug": {

    },
    "br": {

    },
    "bg": {

    },
    "rg": {

    },
}