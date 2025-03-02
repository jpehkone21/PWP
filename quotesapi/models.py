"""
Database models are defined here
"""

from sqlalchemy.engine import Engine
from sqlalchemy import event
import click
from flask.cli import with_appcontext
from quotesapi import db

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Creatures(db.Model):
    name = db.Column(db.String(32), nullable=False, unique=True, primary_key=True)
    age = db.Column(db.Integer, nullable=True)
    picture = db.Column(db.String(256), nullable=True)
    type=db.Column(db.String(128), nullable=True)
    special_force=db.Column(db.String(128), nullable=True)

    quotes = db.relationship("Quotes", back_populates="creatures")

    def serialize(self):
        doc = {
            "name" : self.name,
            "age" : self.age,
            "picture" : self.picture,
            "type" : self.type,
            "special_force" : self.special_force,
            #"quotes" :  self.quotes.serialize() # en tiiä onko oikein
        }
        return doc

    def deserialize(self, doc):
        self.name = doc["name"]
        self.age = doc.get("age")
        self.picture = doc.get("picture")
        self.type = doc.get("type")
        self.special_force = doc.get("special_force")
        #self.quotes = doc.get("quotes").deserialize()


    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name"],
            "additionalProperties": False
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Creature's unique name",
            "type": "string"
        }
        props["age"] = {
            "description": "Age of the creature",
            "type": "integer"
        }
        props["picture"] = {
            "description": "Ascii picture of the creature",
            "type": "string"
        }
        props["type"] = {
            "description": "Type of the creature",
            "type": "string"
        }
        props["special_force"] = {
            "description": "Special force of the creature",
            "type": "string"
        }
        return schema

class Humans(db.Model):
    name = db.Column(db.String(32), nullable=False, unique=True, primary_key=True)
    age = db.Column(db.Integer, nullable=True)
    picture = db.Column(db.String(256), nullable=True)
    relation=db.Column(db.String(128), nullable=True)
    hobby=db.Column(db.String(128), nullable=True)

    quotes = db.relationship("Quotes", back_populates="humans")

    def serialize(self):
        doc = {
            "name" : self.name,
            "age" : self.age,
            "picture" : self.picture,
            "relation" : self.relation,
            "hobby" : self.hobby,
            #"quotes" :  self.quotes.serialize() # en tiiä onko oikein 
        }
        return doc

    def deserialize(self, doc):
        self.name = doc["name"]
        self.age = doc.get("age")
        self.picture = doc.get("picture")
        self.relation = doc.get("relation")
        self.hobby = doc.get("hobby")
        #self.quotes = doc.get("quotes").deserialize()

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name"],
            "additionalProperties": False
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Human's unique name",
            "type": "string"
        }
        props["age"] = {
            "description": "Age of the human",
            "type": "integer"
        }
        props["picture"] = {
            "description": "Ascii picture of the human",
            "type": "string"
        }
        props["relation"] = {
            "description": "What relation does the human have, e.g. sister",
            "type": "string"
        }
        props["hobby"] = {
            "description": "The human's hobby",
            "type": "string"
        }
        return schema

class Animals(db.Model):
    name = db.Column(db.String(32), nullable=False, unique=True, primary_key=True)
    age = db.Column(db.Integer, nullable=True)
    picture = db.Column(db.String(256), nullable=True)
    species=db.Column(db.String(128), nullable=True)
    environment=db.Column(db.String(128), nullable=True)

    quotes = db.relationship("Quotes", back_populates="animals")  

    def serialize(self):
        doc = {
            "name" : self.name,
            "age" : self.age,
            "picture" : self.picture,
            "species" : self.species,
            "environment" : self.environment,
            #"quotes" :  self.quotes.serialize() # en tiiä onko oikein 
        }
        return doc

    def deserialize(self, doc):
        self.name = doc["name"]
        self.age = doc.get("age")
        self.picture = doc.get("picture")
        self.species = doc.get("species")
        self.environment = doc.get("environment")
        #self.quotes = doc.get("quotes").deserialize()

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name"],
            "additionalProperties": False
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Animal's unique name",
            "type": "string"
        }
        props["age"] = {
            "description": "Age of the animal",
            "type": "integer"
        }
        props["picture"] = {
            "description": "Ascii picture of the animal",
            "type": "string"
        }
        props["species"] = {
            "description": "Species of the animal",
            "type": "string"
        }
        props["environment"] = {
            "description": "Environment where the animal lives",
            "type": "string"
        }
        return schema

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(256), nullable=False, unique=True)
    mood = db.Column(db.Float, nullable=False)

    creature_name = db.Column(db.String, db.ForeignKey('creatures.name'), nullable=True)
    human_name = db.Column(db.String, db.ForeignKey('humans.name'), nullable=True)
    animal_name = db.Column(db.String, db.ForeignKey('animals.name'), nullable=True)

    # This constraint is from chatgpt
    # Enforce that only one name is provided
    __table_args__ = (
        db.CheckConstraint(
            "(creature_name IS NOT NULL) + (human_name IS NOT NULL) + (animal_name IS NOT NULL) = 1",
            name="check_only_one_entity"
        ),
    )

    creatures = db.relationship("Creatures", back_populates="quotes")
    humans = db.relationship("Humans", back_populates="quotes")
    animals = db.relationship("Animals", back_populates="quotes")

    def serialize(self):
        doc = {
            "quote" : self.quote,
            "mood" : self.mood
        }
        return doc

    def deserialize(self, doc):
        self.quote = doc["quote"]
        self.mood = doc["mood"]

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["quote", "mood"],
            #"additionalProperties": False
        }
        props = schema["properties"] = {}
        props["quote"] = {
            "description": "written quote",
            "type": "string"
        }
        props["mood"] = {
            "description": "Mood of the quote as number from 0-10",
            "type": "number"
        }
        return schema


@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
