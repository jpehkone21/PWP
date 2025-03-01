from flask import Blueprint
from flask_restful import Api
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter

from quotesapi.models import Creatures, Humans, Animals, Quotes
from quotesapi.resources.human import HumanCollection, HumanItem
from quotesapi.resources.creature import CreatureCollection, CreatureItem
from quotesapi.resources.animal import AnimalCollection, AnimalItem
from quotesapi.resources.quote import QuoteCollection, QuoteItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(CreatureCollection, "/creatures/")
api.add_resource(HumanCollection, "/humans/")
api.add_resource(AnimalCollection, "/animals/")

# Converters
class CreatureConverter(BaseConverter):
    
    def to_python(self, value):
        creature = Creatures.query.filter_by(name=value).first()  
        if creature is None:
            raise NotFound
        return creature
    
    def to_url(self, value):
        return value.name 
    
class HumanConverter(BaseConverter):
    
    def to_python(self, value):
        human = Humans.query.filter_by(name=value).first()  
        if human is None:
            raise NotFound
        return human
    
    def to_url(self, value):
        return value.name
    
class AnimalConverter(BaseConverter):
    
    def to_python(self, value):
        animal = Animals.query.filter_by(name=value).first()
        if animal is None:
            raise NotFound
        return animal
    
    def to_url(self, value):
        return value.name
    
class QuoteConverter(BaseConverter):
    
    def to_python(self, value):
        quote  = Quotes.query.filter_by(quote=value).first()  
        if quote is None:
            raise NotFound
        return quote
    
    def to_url(self, value):
        return value.name

api.add_resource(CreatureItem, "/creatures/<creature:creature>/")
api.add_resource(HumanItem, "/humans/<human:human>/")
api.add_resource(AnimalItem, "/animals/<animal:animal>/")

api.add_resource(QuoteCollection, "/quotes/")
api.add_resource(QuoteItem, 
    "/creatures/<creature>/quotes/<quote>/",
    "/humans/<humans>/quotes/<quote>/",
    "/animals/<animal>/quotes/<quote>/"
)
