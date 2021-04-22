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
    flash,
    jsonify
)
from flask_mysqldb import MySQL, MySQLdb
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    if 'credential' in session:
        g.credential = session['credential']
        g.id = session['id']
        g.username = session['username']
    else:
        g.credential = None
        
@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        session.pop('credential', None)

        username = request.form['username'].lower()
        password = request.form['password']

        respose = requests.post("http://login:11000/", json = {'username': username, "password": password})

        if respose.json()['credential'] != None:
            session['credential'] = respose.json()['credential']
            session['id'] = respose.json()['id']
            session['username'] = respose.json()['username']
            return redirect(url_for('menu'))

        flash("Błedny login lub hasło")
        #return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/menu')
def menu():
    if not g.credential:
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/users', methods=['GET', 'POST'])
def menu_users():
    if g.credential == 'user':
        return redirect(url_for('login'))

        
    if request.method == 'POST':
        id = request.form['id']
        if id != str(g.id):
            print(type(id), type(g.id), flush=True)
            response_id = requests.post("http://user:12000/user_delete", json = {'id': id})

    response = requests.get("http://user:12000/user_table")
    list = []
    list_id = []
    response = response.json()

    for elem in response:
        list.append([response[str(elem)]['id'], response[str(elem)]['username'], response[str(elem)]['password'], response[str(elem)]['credential']])
        #list_id.append([response[str(elem)]['id']])
    return render_template('users.html', data = list, data2 = list_id)

@app.route('/add_user', methods=['GET', 'POST'])
def menu_add_user():
    if g.credential == 'user':
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
            response = requests.post("http://user:12000/new_user", json = {"username": username, "password": password, "credential": credential})
            if response.json()['status'] == "exist":
                flash("Taki użytkownik już istnieje")
            if response.json()['status'] == "created":
                flash("Pomyślnie utworzono użytkownika")
    return render_template('add_user.html')

@app.route('/cameras')
def cameras():
    return render_template('cameras.html')

@app.route('/stats')
def stats():
    if g.credential == 'user':
        return redirect(url_for('login'))
    users = requests.get("http://user:12000/user_stats")
    g.number_of_users = users.json()['number_of_users']
    return render_template('stats.html')

@app.route('/myprofile')
def myprofile():
    return render_template('myprofile.html')

if __name__ == '__main__':
    app.run()
