import json
from flask import request, Response, url_for
from flask_restful import Resource
from quotesapi.models import Humans, Quotes
from quotesapi import db
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from sqlalchemy.exc import IntegrityError


class HumanCollection(Resource):

    def get(self):
        humans = Humans.query.all()
        human_list = [{"name": h.name, 
                        "age": h.age, 
                        "picture": h.picture,
                        "relation": h.relation,
                        "hobby": h.hobby} for h in humans]
        return human_list

    def post(self):
        # error cheking
        if request.method != "POST":
            return "POST method required", 415
    
        if not request.is_json:
            return "Request content type must be JSON", 400
        
        try:
            name = request.json["name"]
            age = request.json["age"]
            picture = request.json["picture"]
            relation = request.json["relation"]
            hobby = request.json["hobby"]
        except (ValueError, KeyError):
            return "Incomplete request - missing fields", 400
        
        try:
            age = int(age)
        except (ValueError, TypeError):
            return "Age must be number", 400
        
        if Humans.query.filter_by(name=name).first() is not None:  #katotaanko niin et yhen niminen eläin voi vain olla?
            return "Human already exists", 409
        ## 
        
        new_human = Humans(name=name, 
                             age=age, 
                             picture=picture, 
                             relation=relation,
                             hobby=hobby)
        
        db.session.add(new_human)
        db.session.commit()

        from quotesapi.api import api
        human_uri = api.url_for(HumanItem, human=new_human)
        headers = {"location": human_uri}
        #print(headers)
        return Response(status=201, headers=headers)

        #return "Human added succesfully"


class HumanItem(Resource):

    def get(self, human):
        return human.serialize()

    def put(self, human):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Humans.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e
        # Prevent changing the primary key (name)
        if human.name != request.json["name"]:
            return "Cannot change primary key (name)", 400
        human.deserialize(request.json)
        try:
            db.session.add(human)
            db.session.commit()
        except IntegrityError as e:
            raise Conflict(
                409,
                f"Human with name '{request.json["name"]}' already exists."
            ) from e
        
        return Response(status=204)

    def delete(self, human):
        # Delete all humans's quotes before deleting humanature
        quotes = Quotes.query.join(Humans).filter(
                Quotes.creature_name == human.name
            ).all()
        if len(quotes) > 0:
            for quote in quotes:
                db.session.delete(quote)
        db.session.delete(human)
        db.session.commit()

        return Response(status=204)