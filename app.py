import requests

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    json,
    flash
)
from flask_mysqldb import MySQL, MySQLdb
from flask_restful import reqparse, abort, Api, Resource

import users_api
import cameras_api
import stats_api
import profile_api

#Backend_api 
be_api = "http://localhost:5000"

app = Flask(__name__)

app.config['MYSQL_USER'] = '19294_zpi'
app.config['MYSQL_PASSWORD'] = 'zpipwr2021'
app.config['MYSQL_DB'] = '19294_zpi'
app.config['MYSQL_HOST'] = 'zpipwr2021.atthost24.pl'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

users_api.init_api(app, mysql)
cameras_api.init_api(app)
profile_api.init_api(app)
stats_api.init_api(app)

app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Users WHERE username=%s",(username,))
        user = cur.fetchone()
        cur.close()
        g.user = user['username']
        g.credentials = user['credential']
        g.id = user['id']
    else:
        g.user = None
        
@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        session.pop('username', None)

        username = request.form['username'].lower()
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Users WHERE username=%s",(username,))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            if password == user['password']:
                session['username'] = user['username']
                return redirect(url_for('menu'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/menu')
def menu():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/menu/users', methods=['GET', 'POST'])
def menu_users():
    if g.credentials == 'user':
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username_add'].lower()
        password = request.form['password_add']
        password2 = request.form['password_add2']
        credential = request.form['credentials_select']
        if credential == 'Użytkownik':
            credential = 'user'
        elif credential == 'Administrator':
            credential = 'admin'
        elif credential == 'Operator':
            credential = 'operator'

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Users WHERE username=%s",(username.lower(),))
        user = cur.fetchone()
        cur.close()

        if user == None:
            if password != password2:
                flash("Hasła nie są jednakowe")
            else:
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO Users (username, password, credential) VALUES (%s, %s, %s)',(username, password, credential))    
                mysql.connection.commit()
                flash("Pomyślnie utworzono użytkownika")
        else:
            flash(f"Taki użytkownik już istnieje", "info")
    return render_template('users.html')

@app.route('/menu/add_user', methods=['GET', 'POST'])
def menu_add_user():
    if g.credentials == 'user':
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username_add'].lower()
        password = request.form['password_add']
        password2 = request.form['password_add2']
        credential = request.form['credentials_select']
        if credential == 'Użytkownik':
            credential = 'user'
        elif credential == 'Administrator':
            credential = 'admin'
        elif credential == 'Operator':
            credential = 'operator'

        if password != password2:
            flash("Hasła nie są jednakowe")
        else:
            r = requests.post(f"{be_api}/users", data={"username": username, "password": password, "credential": credential})
            response = r.json()
            flash(f"response status: {response}")


    return render_template('add_user.html')

@app.route('/menu/cameras', methods=['GET', 'POST'])
def menu_cameras():
    r = requests.get(f"{be_api}/cameras")
    response = r.text
    flash(f"response status: {response}")

    return render_template('cameras.html')
    
@app.route('/menu/myprofile', methods=['GET', 'POST'])
def menu_myprofile():
    r = requests.get(f"{be_api}/myprofile")
    response = r.text
    flash(f"response status: {response}")

    return render_template('myprofile.html')

@app.route('/menu/stats', methods=['GET', 'POST'])
def menu_stats():
    r = requests.get(f"{be_api}/stats")
    response = r.text
    flash(f"response status: {response}")

    return render_template('stats.html')


if __name__ == '__main__':
    app.run()
