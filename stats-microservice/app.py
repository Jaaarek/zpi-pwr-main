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

@app.route('/user_stats', methods = ['GET'])
def user_stats():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT COUNT(username) FROM Users")
    res=cur.fetchall()    
    return jsonify({'number_of_users': res[0]['COUNT(username)']})
    

if __name__ == '__main__':
    app.run()
