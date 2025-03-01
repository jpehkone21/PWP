
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter

from quotesapi.models import Creatures, Humans, Animals, Quotes


# Converters
class CreatureConverter(BaseConverter):
    
    def to_python(self, value):
        creature = Creatures.query.filter_by(name=value).first()  
        if creature is None:
            raise NotFound
        print("creature converter")
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