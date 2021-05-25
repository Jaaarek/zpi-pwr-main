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

@app.route('/user_logs_add', methods = ['POST'])
def user_logs_add():
    app.config['MYSQL_DB'] = '19294_Logs'
    user_id = request.json['user_id']
    date = request.json['date']
    ip = request.json['ip']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO login_logs (user_id, date, ip) VALUES (%s, %s, %s)',(user_id, date, ip))  
    mysql.connection.commit()
    return jsonify({'status': 'logs_added'})


@app.route('/user_logs', methods = ['GET'])
def user_logs():        
    logs_count = requests.post('http://localhost:13000/logs_count', json = {'user_id': '*'})
    app.config['MYSQL_DB'] = '19294_Statistics'
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    num_of_logs = logs_count.json()['number_of_logs']
    num_of_logs = str(num_of_logs)

    cur.execute('UPDATE General SET logs_num = %s'%(num_of_logs))
    mysql.connection.commit()

    cur.execute("SELECT logs_num FROM General")
    res=cur.fetchall()
    return jsonify({'number_of_logs': res[0]['logs_num']})


@app.route('/logs_count', methods = ['POST'])
def logs_count():
    user_id = request.json['user_id']
    print(user_id, flush = True)
    app.config['MYSQL_DB'] = '19294_Logs'
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if user_id == "*":
        cur.execute('SELECT COUNT(user_id) FROM login_logs')
    else:
        cur.execute('SELECT COUNT(user_id) FROM login_logs WHERE user_id = %s'%(user_id))
    res=cur.fetchall()
    return jsonify({'number_of_logs':res[0]['COUNT(user_id)']})


@app.route('/video_feed', methods = ['POST'])
def logs_count():
    name = request.json['name']
    print(name, flush=True)
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Users WHERE username=%s",(name,))
    user = cur.fetchone()
    cur.close()

    if user == None:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Users name VALUES (%s)',(name,))    
        mysql.connection.commit() 
        return jsonify({"status": "created"}) 
    else:
        return jsonify({"status": "exist"})

    # print(user_id, flush = True)
    # app.config['MYSQL_DB'] = '19294_Logs'
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # if user_id == "*":
    #     cur.execute('SELECT COUNT(user_id) FROM login_logs')
    # else:
    #     cur.execute('SELECT COUNT(user_id) FROM login_logs WHERE user_id = %s'%(user_id))
    # res=cur.fetchall()
    return jsonify({'name':'exist'})





if __name__ == '__main__':
    app.run()
