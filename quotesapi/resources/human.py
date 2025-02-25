import json
from flask import request, Response, url_for
from flask_restful import Resource
from quotesapi.models import Humans


class HumanCollection(Resource):

    def get(self):
        # TODO
        pass

    def post(self):
        # TODO
        pass


class HumanItem(Resource):

    def get(self, human):
        return human.serialize()

    def put(self, human):
        # TODO
        pass

    def delete(self, human):
        # TODO
        pass