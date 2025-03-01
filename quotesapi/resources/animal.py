import json
from flask import request, Response, url_for
from flask_restful import Resource
from quotesapi.models import Animals
from quotesapi import db
#from sensorhub import cache
#from sensorhub.models import Measurement, Sensor
#from sensorhub.utils import SensorhubBuilder, create_error_response, page_key, require_sensor_key


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
        # TODO
        pass

    def delete(self, animal):
        # TODO
        pass