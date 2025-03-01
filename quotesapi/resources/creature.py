import json
from flask import request, Response, url_for
from flask_restful import Resource
from quotesapi.models import Creatures
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
            return "POST method required"
    
        if not request.is_json:
            return "Request content type must be JSON"
        
        try:
            name = request.json["name"]
            age = request.json["age"]
            picture = request.json["picture"]
            type = request.json["type"]
            special_force = request.json["special_force"]
        except (ValueError, KeyError):
            return "Incomplete request - missing fields"
        
        try:
            age = int(age)
        except (ValueError, TypeError):
            return "Age must be number"
        
        if Creatures.query.filter_by(name=name).first() is not None:  #katotaanko niin et yhen niminen eläin voi vain olla?
            return "Creature already exists"
        ## 
        
        new_creature = Creatures(name=name, 
                             age=age, 
                             picture=picture, 
                             type=type,
                             special_force=special_force)
        
        db.session.add(new_creature)
        db.session.commit()

        return "Creature added succesfully"


class CreatureItem(Resource):

    def get(self, creature):
        return creature.serialize()

    def put(self, creature):
        # TODO
        pass

    def delete(self, creature):
        # TODO
        pass