# from __future__ import print_function

# import jsonschema
# import consts

# """
# The schema for how a Deck needs to look to work when it gets posted here (or returned to the user)
# """

# DECK_SCHEMA = {
#     "$schema": "http://json-schema.org/draft-06/schema#",
#     "description": "This object describes an in-progress or finished deck.",
#     "type": "object",
#     "properties": {
#         "format": {
#             "type": "string",
#             "enum": [item for item in consts.FORMATS],
#         },
#         "cards": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "properties": {
#                     "name": {
#                         "type": "string",
#                     },
#                     "quantity": {
#                         "type": "integer",
#                         "minimum": 1,
#                         "maximum": 4,
#                     },
#                     "set": {
#                         "type": "string",
#                         "maxLength": 4,
#                     },
#                     "png": {
#                         "type": "string",
#                         "format": "uri",
#                     },
#                     "usd": {
#                         "type": ["number", "string"],
#                     },
#                 },
#                 "required": [
#                     "name",
#                     "quantity",
#                     "set",
#                     "png"
#                 ],
#                 "additionalProperties": False
#             },
#         },
#         "seed": {
#             "type": "string"
#         },
#         "colors": {
#             "type": "string",
#             "enum": [item for item in consts.COLOR_QUERIES],
#         },
#     },
#     "required": [
#         "cards",
#         "format",
#     ],
#     "additionalProperties": False,
# }

# SELECTION_SCHEMA = {
#     "$schema": "http://json-schema.org/draft-06/schema#",
#     "description": "This object describes a card selection.",
#     "type": "object",
#     "properties": {
#         "name": {
#             "type": "string",
#         },
#         "usd": {
#             "type": ["number", "string"],
#         },
#         "cmc": {
#             "type": "integer",
#         },
#         "png": {
#             "type": "string",
#             "format": "uri",
#         },
#         "colors": {
#             "type": "array",
#             "items": {
#                 "type": "string",
#                 "enum": ["W", "U", "B", "R", "G", "C"],
#             },
#         },
#         "set": {
#             "type": "string",
#         },
#         "max_can_add": {
#             "type": "integer",
#             "minimum": 1,
#             "maximum": 4,
#         },
#     },
#     "required": [
#         "name", "usd", "cmc", "png", "colors", "set"
#     ],
#     "additionalProperties": False
# }


# # TODO: Remove this / move it to real tests later; temp tester for my schema
# TESTER = {
#     "format": "Old School 93-94",
#     "colors": "wu",
#     "cards": [
#         {
#             "name": "Swords to Plowshares",
#             "quantity": 4,
#             "set": "LEA",
#             "png": "https://www.example.com/swords",
#             "usd": 599.59
#         },
#         {
#             "name": "Serra Angel",
#             "quantity": 3,
#             "set": "LEB",
#             "png": "https://www.example.com/serra",
#             "usd": 23,
#         },
#     ],
# }