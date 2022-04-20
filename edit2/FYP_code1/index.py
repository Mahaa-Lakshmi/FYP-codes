from flask import Flask, render_template, request, url_for,redirect
import sqlite3 as sql
import re
import string
import random
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

from firebase import firebase
firebase=firebase.FirebaseApplication("https://svhms-user-details-default-rtdb.firebaseio.com/",None)
import pyrebase
firebaseConfig = {
    'apiKey': "AIzaSyD3-UPt-sP6wPtyDN2TLPHKy5qua-J3_04",
    'authDomain': "svhms-user-details.firebaseapp.com",
    'databaseURL': "https://svhms-user-details-default-rtdb.firebaseio.com",
    'projectId': "svhms-user-details",
    'storageBucket': "svhms-user-details.appspot.com",
    'messagingSenderId': "173656186274",
    'appId': "1:173656186274:web:e944d76486a9017a0026fb",
    'measurementId': "G-XQCNVHNW2W"
  }
firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()



app = Flask(__name__)
activeuser=""
nelist=[]


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/choose_login')
def choose_login():
    return render_template('login.html',msg="")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and len(dict(request.form)) > 0:
        userdata = dict(request.form)
        email = userdata["email"]
        password = userdata["password"]
        try:
            login = auth.sign_in_with_email_and_password(email, password)
            return render_template("userhome.html")

        except:
            msg="Invalid email or password"
            return render_template('login.html',msg=msg)


@app.route('/choose_register')
def choose_register():
    return render_template('register.html',msg="")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST' and len(dict(request.form)) > 0:
        userID=""
        userdata = dict(request.form)
        email = userdata["email"]
        car = userdata["car"]
        model = userdata["model"]
        password = userdata["password"]
        #new_data = {"email": email, "car": car, "model": model, "password": password}
        #print(new_data)
        #firebase.post("/users", new_data)
        try:
            user = auth.create_user_with_email_and_password(email, password)
            userID = user['localId']
            doc_ref=firestore_db.collection(u'users').document(userID).set({'email': email, 'car': car,'model':model,'password':password})
            print(userID)
            return render_template("index.html")
        except:
            msg="Email already exists"
            return render_template('register.html',msg=msg)



if __name__ == '__main__':
    app.run(debug=True)