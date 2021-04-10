import requests

from flask_mysqldb import MySQL, MySQLdb
from flask_restful import reqparse, abort, Api, Resource

api = None
mysql = None


class Cameras():
    def get(self):
        return {'status': "OK"}

    def post(self):
        status = "undefined"
        return {'status': status}

def __init__(main):
    def init_api(app):
        global api


    api = Api(app)
