"""
Animal resource
"""
from flask import request, Response
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import Conflict, BadRequest, UnsupportedMediaType
from sqlalchemy.exc import IntegrityError
from quotesapi.models import Animals, Quotes
from quotesapi import db


class AnimalCollection(Resource):
    """
    Implements API operations GET (retrieving all animals) and POST
    """

    def get(self):
        """
        Retrieves all animals in the database and returns them as a list of dictionaries
        """
        animals = Animals.query.all()
        animal_list = [{"name": a.name,
                        "age": a.age, 
                        "picture": a.picture,
                        "species": a.species,
                        "environment": a.environment} for a in animals]
        return animal_list

    def post(self):
        """
        Posting a new animal with all of its information to the database
        """
        # error cheking
        if request.method != "POST":
            return "POST method required", 415

        if not request.is_json:
            return "Request content type must be JSON", 400

        try:
            name = request.json["name"]
            age = request.json["age"]
            picture = request.json["picture"]
            species = request.json["species"]
            environment = request.json["environment"]
        except (ValueError, KeyError):
            return "Incomplete request - missing fields", 400

        try:
            age = int(age)
        except (ValueError, TypeError):
            return "Age must be number", 400

        if Animals.query.filter_by(name=name).first() is not None:
            return "Animal already exists", 409

        new_animal = Animals(name=name,
                             age=age,
                             picture=picture,
                             species=species,
                             environment=environment)

        db.session.add(new_animal)
        db.session.commit()
        from quotesapi.api import api
        animal_uri = api.url_for(AnimalItem, animal=new_animal)
        headers = {"location": animal_uri}
        #print(headers)
        return Response(status=201, headers=headers)

        #return "Animal added succesfully"

class AnimalItem(Resource):
    """
    Implements API operations GET, PUT and DELETE
    """

    def get(self, animal):
        """
        Retrieves details of a specific animal
        """
        return animal.serialize()

    def put(self, animal):
        """
        Updates the details of the specific animal
        """
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Animals.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        # Prevent changing the primary key (name)
        if animal.name != request.json["name"]:
            return "Cannot change primary key (name)", 400
        animal.deserialize(request.json)
        try:
            db.session.add(animal)
            db.session.commit()
        except IntegrityError as e:
            raise Conflict(
                409,
                #f"Animal with name '{request.json["name"]}' already exists."
                f"Animal with name \"{request.json['name']}\" already exists."
            ) from e

        return Response(status=204)


    def delete(self, animal):
        """
        Deletes the animal from the database
        """
        # Delete all animal's quotes before deleting animal
        quotes = Quotes.query.join(Animals).filter(
                Quotes.creature_name == animal.name
            ).all()
        if len(quotes) > 0:
            for quote in quotes:
                db.session.delete(quote)
        db.session.delete(animal)
        db.session.commit()

        return Response(status=204)
