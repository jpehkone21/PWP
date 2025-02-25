import json
from flask import request, Response, url_for
from flask_restful import Resource
from quotesapi.models import Creatures

class CreatureCollection(Resource):

    def get(self):
        # TODO
        pass

    def post(self):
        # TODO
        pass


class CreatureItem(Resource):

    def get(self, creature):
        return creature.serialize()

    def put(self, creature):
        # TODO
        pass

    def delete(self, creature):
        # TODO
        pass