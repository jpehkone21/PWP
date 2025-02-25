import json
from flask import request, Response, url_for
from flask_restful import Resource
from quotesapi.models import Quotes


class QuoteCollection(Resource):

    def get(self):
        # TODO
        pass

    def post(self):
        # TODO
        pass


class QuoteItem(Resource):

    def get(self, quote):
        return quote.serialize()

    def put(self, quote):
        # TODO
        pass

    def delete(self, quote):
        # TODO
        pass