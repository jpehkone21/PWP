import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'quotes_database.db')
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

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
        # TODO
        pass

    def deserialize(self):
        # TODO
        pass


    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name"]
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
        # TODO Need to continue this...
        return schema

class Humans(db.Model):
    name = db.Column(db.String(32), nullable=False, unique=True, primary_key=True)
    age = db.Column(db.Integer, nullable=True)
    picture = db.Column(db.String(256), nullable=True)
    relation=db.Column(db.String(128), nullable=True)
    hobby=db.Column(db.String(128), nullable=True)
    
    quotes = db.relationship("Quotes", back_populates="humans")

    def serialize(self):
        # TODO
        pass

    def deserialize(self):
        # TODO
        pass

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name"]
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
        # TODO Need to continue this...
        return schema

class Animals(db.Model):
    name = db.Column(db.String(32), nullable=False, unique=True, primary_key=True)
    age = db.Column(db.Integer, nullable=True)
    picture = db.Column(db.String(256), nullable=True)
    species=db.Column(db.String(128), nullable=True)
    environment=db.Column(db.String(128), nullable=True)
    
    quotes = db.relationship("Quotes", back_populates="animals")  

    def serialize(self):
        # TODO
        pass

    def deserialize(self):
        # TODO
        pass

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name"]
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
        # TODO Need to continue this...
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
        # TODO
        pass

    def deserialize(self):
        # TODO
        pass

    @staticmethod
    def json_schema():
        # TODO Need to continue this...
        pass
   