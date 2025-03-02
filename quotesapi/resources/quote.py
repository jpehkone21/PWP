"""
Quote resource
"""
from flask import request, Response
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import Conflict, BadRequest, UnsupportedMediaType
from sqlalchemy.exc import IntegrityError
from quotesapi.models import Quotes, Animals, Creatures, Humans
from quotesapi import db


class QuoteCollection(Resource):

    def get(self, animal=None, creature=None, human=None):
        #quotes = Quotes.query.all()
        quotes = []
        quote_list = []

        if creature is not None:
            quotes = Quotes.query.join(Creatures).filter(
                Quotes.creature_name == creature
            ).all()
            #return quotes
        if human is not None:
            quotes = Quotes.query.join(Humans).filter(
                Quotes.human_name == human
            ).all()
            #return quotes
        if animal is not None:
            quotes = Quotes.query.join(Animals).filter(
                Quotes.animal_name == animal
            ).all()
            #return quotes
        for quote in quotes:
            quote_list.append(quote.serialize())

        return quote_list

    def post(self, animal=None, creature=None, human=None):
        # error cheking
        if request.method != "POST":
            return "POST method required", 415

        if not request.is_json:
            return "Request content type must be JSON", 400

        try:
            #id = request.json["id"]
            quote = request.json["quote"]
            mood = request.json["mood"]
            #entity = request.json["entity"]
        except (ValueError, KeyError):
            return "Incomplete request - missing fields", 400

        try:
            #id = int(id)
            mood = float(mood)
        except (ValueError, TypeError):
            return "mood must be number", 400

        if Quotes.query.filter_by(quote=quote).first() is not None:
            return "Quote with this text already exists", 409
        new_quote = None
        # print(creature)
        if animal is not None:
            animal_obj = Animals.query.filter_by(name=animal).first()
            new_quote = Quotes(#id=id, 
                             quote=quote, 
                             mood=mood,
                             animals=animal_obj 
                             #entity=entity
                            )
        if creature is not None:
            creature_obj = Creatures.query.filter_by(name=creature).first()
            new_quote = Quotes(quote=quote,
                             mood=mood,
                             creatures=creature_obj
                             #entity=entity
                            )
        if human is not None:
            human_obj = Humans.query.filter_by(name=human).first()
            new_quote = Quotes(
                             quote=quote,
                             mood=mood,
                             humans=human_obj
                             #entity=entity
                            )

        db.session.add(new_quote)
        db.session.commit()

        #quote_uri = api.url_for(QuoteItem, creature=creature, quote=new_quote.id)
        #headers = {"location": quote_uri}
        #print(headers)
        #return Response(status=201, headers=headers)

        return "Quote added succesfully", 201


class QuoteItem(Resource):

    def get(self, quote, animal=None, creature=None, human=None):
        return quote.serialize()

    def put(self, quote, animal=None, creature=None, human=None):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Quotes.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e
        if Quotes.query.filter_by(quote=request.json["quote"]).first() is not None:
            return "Quote with this text already exists", 400
        quote.deserialize(request.json)
        try:
            db.session.add(quote)
            db.session.commit()
        except IntegrityError as e:
            raise Conflict(
                409,
                "Integrityerror."
            ) from e

        return Response(status=204)

    def delete(self, quote, animal=None, creature=None, human=None):
        db.session.delete(quote)
        db.session.commit()

        return Response(status=204)
