from flask import Flask, jsonify, request
import requests

from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

app.config['MYSQL_USER'] = '19294'
app.config['MYSQL_PASSWORD'] = 'zpipwr2021'
app.config['MYSQL_HOST'] = 'zpipwr2021.atthost24.pl'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/user_stats', methods = ['GET'])
def user_stats():
    app.config['MYSQL_DB'] = '19294_zpi'
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT COUNT(username) FROM Users")
    res=cur.fetchall()    
    return jsonify({'number_of_users': res[0]['COUNT(username)']})

@app.route('/user_logs', methods = ['POST', 'GET'])
def user_logs():
    if request.method == 'POST':
        app.config['MYSQL_DB'] = '19294_Statistics'
        user_id = request.json['user_id']
        date = request.json['date']
        ip = request.json['ip']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO login_logs (user_id, date, ip) VALUES (%s, %s, %s)',(user_id, date, ip))  
        mysql.connection.commit()

    if request.method == 'GET':
        app.config['MYSQL_DB'] = '19294_Statistics'
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT COUNT(user_id) FROM login_logs")
        res=cur.fetchall()    
        return jsonify({'number_of_logs': res[0]['COUNT(user_id)']})


    

if __name__ == '__main__':
    app.run()
