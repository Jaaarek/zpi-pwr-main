from flask import Flask, jsonify, request
import requests

from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

app.config['MYSQL_USER'] = '19294_zpi'
app.config['MYSQL_PASSWORD'] = 'zpipwr2021'
app.config['MYSQL_DB'] = '19294_zpi'
app.config['MYSQL_HOST'] = 'zpipwr2021.atthost24.pl'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Users WHERE username=%s",(username,))
    user = cur.fetchone()
    cur.close()
    if user:
        if password == user['password']:
            return jsonify({'credential': user['credential'], 'id': user['id'], 'username': user['username']})

    return jsonify({"credential": None})


if __name__ == '__main__':
    app.run()
