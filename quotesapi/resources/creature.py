"""
Creature resource
"""
from flask import request, Response
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import Conflict, BadRequest, UnsupportedMediaType
from sqlalchemy.exc import IntegrityError
from quotesapi.models import Creatures, Quotes
from quotesapi import db

class CreatureCollection(Resource):

    def get(self):
        creatures = Creatures.query.all()
        creature_list = [{"name": c.name,
                        "age": c.age, 
                        "picture": c.picture,
                        "type": c.type,
                        "special_force": c.special_force} for c in creatures]
        return creature_list

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
            type = request.json["type"]
            special_force = request.json["special_force"]
        except (ValueError, KeyError):
            return "Incomplete request - missing fields", 400

        try:
            age = int(age)
        except (ValueError, TypeError):
            return "Age must be number", 400

        if Creatures.query.filter_by(name=name).first() is not None:
            return "Creature already exists", 409

        new_creature = Creatures(name=name,
                             age=age,
                             picture=picture,
                             type=type,
                             special_force=special_force)
        
        db.session.add(new_creature)
        db.session.commit()

        from quotesapi.api import api
        creature_uri = api.url_for(CreatureItem, creature=new_creature)
        headers = {"location": creature_uri}
        #print(headers)
        return Response(status=201, headers=headers)
        #return "Creature added succesfully"


class CreatureItem(Resource):

    def get(self, creature):
        return creature.serialize()

    def put(self, creature):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Creatures.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        # Prevent changing the primary key (name)
        if creature.name != request.json["name"]:
            return "Cannot change primary key (name)", 400

        creature.deserialize(request.json)
        try:
            db.session.add(creature)
            db.session.commit()
        except IntegrityError as e:
            raise Conflict(
                409,
                f"Creature with name '{request.json["name"]}' already exists."
            ) from e

        return Response(status=204)

    def delete(self, creature):

        # Delete all creature's quotes before deleting creature
        quotes = Quotes.query.join(Creatures).filter(
                Quotes.creature_name == creature.name
            ).all()
        if len(quotes) > 0:
            for quote in quotes:
                db.session.delete(quote)
        db.session.delete(creature)
        db.session.commit()

        return Response(status=204)
