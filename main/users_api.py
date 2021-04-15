import requests

from flask_mysqldb import MySQL, MySQLdb
from flask_restful import reqparse, abort, Api, Resource

api = None
mysql = None

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('credential')

class Users(Resource):
    def get(self):
        return {'status': "OK"}

    def post(self):
        status = "undefined"

        args = parser.parse_args()
        print(f"args = {args}")
        username = args['username']
        password = args['password']
        credential = args['credential']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Users WHERE username=%s",(username.lower(),))
        user = cur.fetchone()
        cur.close()

        if user == None:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO Users (username, password, credential) VALUES (%s, %s, %s)',(username, password, credential))    
            mysql.connection.commit()
            status = "created"    
        else:
            status = "exists"

        return {'status': status}

def init_api(app, _mysql):
    global api
    global mysql

    api = Api(app)
    mysql = _mysql
    api.add_resource(Users, '/users')
