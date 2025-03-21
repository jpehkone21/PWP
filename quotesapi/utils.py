"""
Url converters are here
"""
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter

from quotesapi.models import Creatures, Humans, Animals, Quotes


# Converters
class CreatureConverter(BaseConverter):
    """
    URL converter for converting between creature's name and the corresponding Creatures model
    """
    def to_python(self, value):
        creature = Creatures.query.filter_by(name=value).first()
        if creature is None:
            raise NotFound
        print("creature converter")
        return creature

    def to_url(self, value):
        return value.name

class HumanConverter(BaseConverter):
    """
    URL converter for converting between human's name and the corresponding Human model
    """
    def to_python(self, value):
        human = Humans.query.filter_by(name=value).first()
        if human is None:
            raise NotFound
        return human

    def to_url(self, value):
        return value.name

class AnimalConverter(BaseConverter):
    """
    URL converter for converting between animal's name and the corresponding Animal model
    """
    def to_python(self, value):
        animal = Animals.query.filter_by(name=value).first()
        if animal is None:
            raise NotFound
        return animal

    def to_url(self, value):
        return value.name

class QuoteConverter(BaseConverter):
    """
    URL converter for converting between quote's id and the corresponding Quotes model
    """
    def to_python(self, value):
        quote  = Quotes.query.filter_by(id=value).first()
        if quote is None:
            raise NotFound
        print("quote converter")
        return quote

    def to_url(self, value):
        return value.name
