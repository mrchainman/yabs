#!/usr/bin/python
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session

from forms import RegistrationForm, User, LoginForm

app = Flask(__name__)
app.secret_key = "73f5380b1ed83164de149ccfe3d1d9f813e40bdc81b2f447f0db3e8f2299829f"


def check_session(target):
    if "user" not in session:
        return redirect(url_for(target))

def check_creds(username, password):
    db_users, db_passwords = setup_db('''SELECT username,password FROM users''')
    if username in db_users and password in db_passwords:
        return True

def setup_db(query):
    with sqlite3.connect('test.db') as con:
        cur = con.cursor()
        cur.execute(query)


@app.route("/")
def home():
    check_session("login")
    return render_template("home.html", name=session["user"])

@app.route("/login/")
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if check_creds(form.username.data, form.password.data) == True:
            session["user"] = form.username.data
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/register/", methods=['GET', 'POST'])
def register():
    check_session("login")
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        session["user"] = user.username
        setup_db(f'''INSERT INTO users VALUES ("{user.username}", "{user.email}", "{user.password}")''')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    setup_db('''CREATE TABLE IF NOT EXISTS users (username text, email text, password text);''')
    app.run(debug=True)
