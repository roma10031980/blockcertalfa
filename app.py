from flask import Flask, url_for, redirect, request, render_template, session
from pymongo import MongoClient
import os
import datetime
from flask_bcrypt import Bcrypt
global role_name
bcrypt = Bcrypt(None)
app = Flask(__name__, template_folder="templates")
app.secret_key = "@$TA;VNSKJOWIAJFLSKDJVZSLKDlskja;sX,CMN"
#app.config['SECRET_KEY'] = '$BUDehtise98&8*login\/m#/./there#$@fier__more__thies1~87'
# client = MongoClient(os.environ['BLOCKCERTALFA_DB_1_PORT_27017_TCP_ADDR'], 27017)
# db = client.blockcertdb
#mongodb://user:password@localhost:27017/dbname

# connect_string = "mongodb://root:root2017.@BLOCKCERTALFA_DB_1_PORT_27017_TCP_ADDR:27017/blockcertdb"
# ModelUsers = MongoClient(connect_string)
# Musers = ModelUsers.users
client = MongoClient(os.environ['BLOCKCERTALFA_DB_1_PORT_27017_TCP_ADDR'], 27017)
Musers = client.blockcertdb


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_name = request.form['username']
    user_pass = request.form['password']
    _user_name = Musers.users.find({"email": user_name}).count()
    _user_pass = Musers.users.find({"password": user_pass}).count()
    if _user_name == 1 and _user_pass == 1:
        session['logged_in'] = True
        usernamesession = []
        usernamesession.append(user_name)
        return redirect(url_for('dashboard'))
    else:
        error = 1
        return render_template('index.html', errors=error)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    # user_name = request.form['username']
    # user_pass = request.form['password']
    # _user_name = Musers.users.find({"email": user_name}).count()
    # cursor = Musers.users.find_one({"email": user_name})
    # password = bcrypt.check_password_hash(cursor['password'], user_pass)
    # if _user_name == 1 and password == True:
    #     username = Musers.users.find({"email": user_name})
    #     session['logged_in'] = True
    #     return render_template('dashboard.html', usernames=username)
    # else:
    #     error = 1
    #     return render_template('index.html', errors=error)
    return render_template('dashboard.html')


@app.route('/users')
def users():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        _musers = Musers.users.find()
        musers = [musers for musers in _musers]
        return render_template('users.html', musers=musers)


@app.route('/register', methods=['POST'])
def register():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        roleid = request.form['roleid']

        if roleid == "1":
            role_name = "admin"

        if roleid == "2":
            role_name = "Entidad Universitaria"

        if roleid == "3":
            role_name = "Entidad Personal"

        current_date = str(datetime.datetime.now())
        password_hash = bcrypt.generate_password_hash(request.form['password'])
        item_user = {
            'name': request.form['name'],
            'lastname': request.form['lastname'],
            'email': request.form['email'],
            'password': password_hash,
            'roleid': request.form['roleid'],
            'rolename': role_name,
            'status': request.form['status'],
            'created_at': current_date
        }

        Musers.users.insert_one(item_user)

        return redirect(url_for('users'))


@app.route('/cert-tools')
def certtools():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('cert-tools.html')


@app.route('/create-certs')
def createcerts():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('create-certs.html')


@app.route('/verfication-certs')
def verificationcerts():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('verification-certs.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
