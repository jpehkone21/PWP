import json
from flask import request, Response, url_for
from flask_restful import Resource
from quotesapi.models import Humans
from quotesapi import db


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
            return "POST method required"
    
        if not request.is_json:
            return "Request content type must be JSON"
        
        try:
            name = request.json["name"]
            age = request.json["age"]
            picture = request.json["picture"]
            relation = request.json["relation"]
            hobby = request.json["hobby"]
        except (ValueError, KeyError):
            return "Incomplete request - missing fields"
        
        try:
            age = int(age)
        except (ValueError, TypeError):
            return "Age must be number"
        
        if Humans.query.filter_by(name=name).first() is not None:  #katotaanko niin et yhen niminen eläin voi vain olla?
            return "Human already exists"
        ## 
        
        new_human = Humans(name=name, 
                             age=age, 
                             picture=picture, 
                             relation=relation,
                             hobby=hobby)
        
        db.session.add(new_human)
        db.session.commit()

        return "Human added succesfully"


class HumanItem(Resource):

    def get(self, human):
        return human.serialize()

    def put(self, human):
        # TODO
        pass

    def delete(self, human):
        # TODO
        pass