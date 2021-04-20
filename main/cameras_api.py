import requests
from flask_restful import reqparse, abort, Api, Resource

api = None

class Cameras(Resource):
    def get(self):
        return {'status': "OK"}

    def post(self):
        return {'status': "OK"}

def init_api(app):
    global api
    
    api = Api(app)
    api.add_resource(Cameras, '/cameras')
