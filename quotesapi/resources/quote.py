import json
from flask import request, Response, url_for, jsonify
from flask_restful import Resource
from quotesapi.models import Quotes, Animals, Creatures, Humans
from quotesapi import db
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from sqlalchemy.exc import IntegrityError


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
        '''
        
        
        # This for-loop is from chatgpt
        # Determining which entity the quote belongs to
        for q in quotes:
            entity = None
            if q.creature_name:
                entity = {"type": "creature", "name": q.creature_name}
            elif q.human_name:
                entity = {"type": "human", "name": q.human_name}
            elif q.animal_name:
                entity = {"type": "animal", "name": q.animal_name}
                
            quote_list.append({"id": q.id,
                            "quote": q.quote,
                            "mood": q.mood,
                            "entity": entity})  #en oo varma onko oikein näin liittää quote johonki hahmoon
        '''
        return quote_list

    def post(self, animal=None, creature=None, human=None):
        # error cheking
        if request.method != "POST":
            return "POST method required"
    
        if not request.is_json:
            return "Request content type must be JSON"
        
        try:
            #id = request.json["id"]
            quote = request.json["quote"]
            mood = request.json["mood"]
            #entity = request.json["entity"]
        except (ValueError, KeyError):
            return "Incomplete request - missing fields"
        
        try:
            #id = int(id)
            mood = float(mood)
        except (ValueError, TypeError):
            return "ID and mood must be numbers"
        
        if Quotes.query.filter_by(quote=quote).first() is not None:  #katotaanko niin et yhen niminen eläin voi vain olla?
            return "Quote with this ID already exists"
        ## 
        
        '''new_quote = Quotes(#id=id, 
                             quote=quote, 
                             mood=mood, 
                             #entity=entity
                            )'''
        print(creature)
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
            new_quote = Quotes(#id=id, 
                             quote=quote, 
                             mood=mood,
                             humans=human_obj
                             #entity=entity
                            )
        
        db.session.add(new_quote)
        db.session.commit()

        return "Quote added succesfully"


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
        # TODO
        pass