import json
from flask import request, Response, url_for
from flask_restful import Resource
from quotesapi.models import Animals
#from sensorhub import cache
#from sensorhub.models import Measurement, Sensor
#from sensorhub.utils import SensorhubBuilder, create_error_response, page_key, require_sensor_key


class AnimalCollection(Resource):

    def get(self):
        # TODO
        pass

    def post(self):
        # TODO
        pass


class AnimalItem(Resource):

    def get(self, animal):
        return animal.serialize()

    def put(self, animal):
        # TODO
        pass

    def delete(self, animal):
        # TODO
        pass