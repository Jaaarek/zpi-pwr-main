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


@app.route('/user_table', methods = ['GET'])
def user_table():
    x = {}
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Users")
    i = 1
    res=cur.fetchall()
    for row in res:
        x[i] = row
        i+=1
    return jsonify(x)

@app.route('/new_user', methods=['POST'])
def new_user():
    username = request.json['username']
    password = request.json['password']
    credential = request.json['credential'] 
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Users WHERE username=%s"%(username.lower(),))
    user = cur.fetchone()
    cur.close()
    if user == None:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Users (username, password, credential) VALUES (%s, %s, %s)'%(username, password, credential))    
        mysql.connection.commit() 
        return jsonify({"status": "created"}) 
    else:
        return jsonify({"status": "exist"})

@app.route('/user_delete', methods=['POST'])
def user_delete():
    id = request.json['id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM Users WHERE id=%s"%id)
    mysql.connection.commit() 
    return jsonify({'status': 'deleted'})

@app.route('/user_change_name', methods=['POST'])
def user_change_name():
    username = request.json['new_username']
    id = request.json['id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Users WHERE username=%s"%(username.lower(),))
    user = cur.fetchone()
    if user == None:
        cur.execute("UPDATE Users SET username = \'%s\' WHERE id = %s"%(username, id))
        mysql.connection.commit() 
        return jsonify({'status': 'changed'})
    else:
        return jsonify({'status': 'exists'})

@app.route('/user_change_password', methods=['POST'])
def user_change_password():
    password = request.json['new_password']
    id = request.json['id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("UPDATE Users SET password = \'%s\' WHERE id = %s"%(password, id))
    mysql.connection.commit() 
    return jsonify({'status': 'changed'})

if __name__ == '__main__':
    app.run()
