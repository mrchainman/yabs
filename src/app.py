#!/usr/bin/python
from flask import Flask, render_template, request, flash, redirect, url_for
from forms import RegistrationForm, User

app = Flask(__name__)
app.secret_key = "73f5380b1ed83164de149ccfe3d1d9f813e40bdc81b2f447f0db3e8f2299829f"

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login/")
def login():
    return render_template("login.html")


@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        flash(f"""
        Thanks for registering!
        Here is the Data you inputted:
        Username: {user.username}
        Email: {user.email}
        Password: {user.password}
        """)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
