import json
from flask import request, Response, url_for
from flask_restful import Resource
from quotesapi.models import Animals
from quotesapi import db
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from sqlalchemy.exc import IntegrityError


class AnimalCollection(Resource):

    def get(self):
        animals = Animals.query.all()
        animal_list = [{"name": a.name, 
                        "age": a.age, 
                        "picture": a.picture,
                        "species": a.species,
                        "environment": a.environment} for a in animals]
        return animal_list

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
            species = request.json["species"]
            environment = request.json["environment"]
        except (ValueError, KeyError):
            return "Incomplete request - missing fields"
        
        try:
            age = int(age)
        except (ValueError, TypeError):
            return "Age must be number"
        
        if Animals.query.filter_by(name=name).first() is not None:  #katotaanko niin et yhen niminen eläin voi vain olla?
            return "Animal already exists"
        ## 
        
        new_animal = Animals(name=name, 
                             age=age, 
                             picture=picture, 
                             species=species,
                             environment=environment)
        
        db.session.add(new_animal)
        db.session.commit()

        return "Animal added succesfully"

class AnimalItem(Resource):

    def get(self, animal):
        return animal.serialize()

    def put(self, animal):
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Animals.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        animal.deserialize(request.json)
        try:
            db.session.add(animal)
            db.session.commit()
        except IntegrityError as e:
            raise Conflict(
                409,
                f"Animal with name '{request.json["name"]}' already exists."
            ) from e
        
        return Response(status=204)


    def delete(self, animal):
        # TODO
        pass