import json
from flask import request, Response, url_for
from flask_restful import Resource
from quotesapi.models import Quotes
from quotesapi import db


class QuoteCollection(Resource):

    def get(self):
        quotes = Quotes.query.all()
        quote_list = []
        
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
        
        return quote_list

    def post(self):
        # error cheking
        if request.method != "POST":
            return "POST method required"
    
        if not request.is_json:
            return "Request content type must be JSON"
        
        try:
            id = request.json["id"]
            quote = request.json["quote"]
            mood = request.json["mood"]
            entity = request.json["entity"]
        except (ValueError, KeyError):
            return "Incomplete request - missing fields"
        
        try:
            id = int(id)
            mood = float(mood)
        except (ValueError, TypeError):
            return "ID and mood must be numbers"
        
        if Quotes.query.filter_by(id=id).first() is not None:  #katotaanko niin et yhen niminen eläin voi vain olla?
            return "Quote with this ID already exists"
        ## 
        
        new_quote = Quotes(id=id, 
                             quote=quote, 
                             mood=mood, 
                             entity=entity)
        
        db.session.add(new_quote)
        db.session.commit()

        return "Quote added succesfully"


class QuoteItem(Resource):

    def get(self, quote):
        return quote.serialize()

    def put(self, quote):
        # TODO
        pass

    def delete(self, quote):
        # TODO
        pass