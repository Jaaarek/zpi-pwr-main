import requests
from flask_restful import reqparse, abort, Api, Resource

api = None

class Stats(Resource):
    def get(self):
        return "OK"

    def post(self):
        return "OK"

def init_api(app):
    global api

    api = Api(app)
    api.add_resource(Stats, '/statistics')
