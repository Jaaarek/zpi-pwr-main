import requests
from authlib.integrations.flask_client import OAuth
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
from datetime import datetime

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
    return redirect(url_for('landing'))

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        session.pop('credential', None)
        username = request.form['username'].lower()
        password = request.form['password']
        respose = requests.post("http://login:11000/", json = {'username': username, "password": password, 'email': None})

        if respose.json()['credential'] != None:
            session['credential'] = respose.json()['credential']
            session['id'] = respose.json()['id']
            session['username'] = respose.json()['username']
            respose = requests.post("http://stats:13000/user_logs_add", json = {'user_id': respose.json()['id'], "date": str(datetime.now()), "ip": request.remote_addr})
            print(str(datetime.now()), request.remote_addr, flush=True)
            return redirect(url_for('menu'))
        flash("Błedny login lub hasło")
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
    users = requests.get("http://stats:13000/user_stats")
    logs = requests.get("http://stats:13000/user_logs")
    # TO NIE DZIAŁA
    # g.number_of_logs = logs.json()['number_of_logs']
    # g.number_of_users = users.json()['number_of_users']
    return render_template('stats.html')


@app.route('/myprofile', methods=['GET', 'POST'])
def myprofile():
    response = requests.post("http://stats:13000/logs_count", json = {"user_id": g.id})
    # TO TEŻ NIE DZIAŁA
    # g.personal_number_of_logs = response.json()['number_of_logs']

    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        new_password2 = request.form['new_password_2']
        if new_username != '':
            response = requests.post("http://user:12000/user_change_name", json = {'new_username': new_username, 'id': g.id})
            if response.json()['status'] == 'changed':
                session['username'] = new_username
                return redirect(url_for('myprofile'))
            elif response.json()['status'] == 'exists':
                flash('Taki użytkownik już istnieje')

        if new_password != '':
            if new_password == new_password2:
                response = requests.post("http://user:12000/user_change_password", json = {'new_password': new_password, 'id': g.id})
                if response.json()['status'] == 'changed':
                    session['username'] = new_username
                    return redirect(url_for('myprofile'))
            else:
                flash('Hasła nie są jednakowe')
    

    return render_template('myprofile.html')

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="1090276623155-avonjnm352om8mskqh6jj4aef276indv.apps.googleusercontent.com",
    client_secret="ATqNHrVoiez3IaTSEvWt-jr7",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',#do wzięcia z dokumentacji
    client_kwargs={'scope': 'openid email'},#scope = co chcemy żeby google zwrócił przez toke i get z /authorize
)

@app.route('/log/google')
def login_google():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize') #jeżeli identyfikacja się udała leci tu
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    #resp.raise_for_status()  //nie wiem co to, z nowszej wersji
    user_info = resp.json()
    # do something with the token and profile
    #user = oauth.google.userinfo() psuje logowanie # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['email'] = user_info['email']
    print(session['email'], flush = True)
    respose = requests.post("http://login:11000/", json = {'username': None, "password": None, 'email': user_info['email']})
    print(respose.json(), flush=True)
    if respose.json()['credential'] != None:
        session['credential'] = respose.json()['credential']
        session['id'] = respose.json()['id']
        session['username'] = respose.json()['username']
        respose = requests.post("http://stats:13000/user_logs_add", json = {'user_id': respose.json()['id'], "date": str(datetime.now()), "ip": request.remote_addr})
        print(str(datetime.now()), request.remote_addr, flush=True)
        return redirect(url_for('menu'))
    flash("Błedny login lub hasło")
    return render_template('login.html')





if __name__ == '__main__':
    app.run()
