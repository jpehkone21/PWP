"""
Url mappings
"""

from flask import Blueprint
from flask_restful import Api
from quotesapi.resources.human import HumanCollection, HumanItem
from quotesapi.resources.creature import CreatureCollection, CreatureItem
from quotesapi.resources.animal import AnimalCollection, AnimalItem
from quotesapi.resources.quote import QuoteCollection, QuoteItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(CreatureCollection, "/creatures/")
api.add_resource(HumanCollection, "/humans/")
api.add_resource(AnimalCollection, "/animals/")



api.add_resource(CreatureItem, "/creatures/<creature:creature>/")
api.add_resource(HumanItem, "/humans/<human:human>/")
api.add_resource(AnimalItem, "/animals/<animal:animal>/")

api.add_resource(QuoteCollection,
    "/quotes/",
    "/creatures/<creature>/quotes/",
    "/humans/<human>/quotes/",
    "/animals/<animal>/quotes/"
)
api.add_resource(QuoteItem,
    "/creatures/<creature>/quotes/<quote:quote>/",
    "/humans/<human>/quotes/<quote:quote>/",
    "/animals/<animal>/quotes/<quote:quote>/"
)
