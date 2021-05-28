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
    email = request.json['email']

    print(username, password, email)

    if username:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Users WHERE username=%s",(username,))
        user = cur.fetchone()
        cur.close()

    if email:
        try:
            print(username, password, email, flush=True)
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM Users WHERE username=\'%s\'"%(email,))
            #cur.execute("SELECT * FROM Users WHERE username=\'adam.fabijan@gmail.com\'")
            user = cur.fetchone()
            cur.close()
            print(user['credential'], flush=True)
        except:
            return jsonify({"credential": None})
    try:
        if user:
            if password == user['password']:
                return jsonify({'credential': user['credential'], 'id': user['id'], 'username': user['username']})
    except: 
        return jsonify({"credential": None})
        
    if email:
        print(user['credential'], flush=True)
        return jsonify({'credential': user['credential'], 'id': user['id'], 'username': user['username']})

    return jsonify({"credential": None})


if __name__ == '__main__':
    app.run()
