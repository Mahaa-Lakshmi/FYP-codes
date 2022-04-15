from flask import Flask, render_template, request, url_for,redirect
import sqlite3 as sql
import re
import string
import random
from firebase import firebase
firebase=firebase.FirebaseApplication("https://svhms-user-details-default-rtdb.firebaseio.com/",None)



app = Flask(__name__)
activeuser=""
nelist=[]


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/choose_login')
def choose_login():
    return render_template('login.html')


@app.route('/choose_register')
def choose_register():
    return render_template('register.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST' and len(dict(request.form)) > 0:
        userdata = dict(request.form)
        email = userdata["email"]
        car = userdata["car"]
        model = userdata["model"]
        password = userdata["password"]
        new_data = {"email": email, "car": car, "model": model, "password": password}
        print(new_data)
        firebase.post("/users", new_data)
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)