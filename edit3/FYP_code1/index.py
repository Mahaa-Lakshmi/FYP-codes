from flask import Flask, render_template, request, url_for,redirect
from classifier import myfunc
import firebase_admin
from firebase_admin import credentials, firestore
from firebase import firebase
import math
import pyrebase
import pandas as pd
import numpy as np


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

firebase=firebase.FirebaseApplication("https://svhms-user-details-default-rtdb.firebaseio.com/",None)
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
storage=firebase.storage()



app = Flask(__name__)
activeuser=""
nelist=[]

def get_df():
    cloudfilename="live27.csv"
    url = storage.child(cloudfilename).get_url(None)
    print(url)
    df = pd.read_csv(url, index_col=False)
    return df

def get_dashboard_values():
    df = get_df()
    send_list_values = []
    send_list_values.append(math.ceil(max(df['ENGINE_RUN_TINE ()']) / 60))
    send_list_values.append(round(max(df['ENGINE_RPM ()']), 2))
    send_list_values.append(round(df['ENGINE_RPM ()'].mean(), 2))
    send_list_values.append(df['ENGINE_RPM ()'].tolist()) #engine rpm
    send_list_values.append(df['ENGINE_RUN_TINE ()'].tolist()) #engine run time
    send_list_values.append(df['VEHICLE_SPEED ()'].tolist()) #engine vehicle speed
    send_list_values.append(df['COOLANT_TEMPERATURE ()'].tolist()) #coolant temp
    send_list_values.append(df['INTAKE_AIR_TEMP ()'].tolist()) #intake temp
    send_list_values.append(round(df['VEHICLE_SPEED ()'].mean(), 2)) #vehicle speed
    return send_list_values

def get_health_values_from_file():
    df=get_df()
    send_list_values=[]
    send_list_values.append(round(df['ENGINE_RPM ()'].mean(), 2))
    send_list_values.append(round(df['INTAKE_AIR_TEMP ()'].mean(), 2))  # intake temp
    send_list_values.append(round(df['COOLANT_TEMPERATURE ()'].mean(), 2))  # coolant temp
    return send_list_values


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
            userID=login['localId']
            doc_ref = firestore_db.collection(u'users').document(userID).get()
            userDetails=doc_ref.to_dict()
            send_list_values=get_dashboard_values()
            return render_template("userhomepage.html",coolant_temp=send_list_values[6],avg_speed=send_list_values[8],intake_air_temp=send_list_values[7],userDetails=userDetails,list_values=send_list_values,engine_rpm=send_list_values[3],engine_runtime=send_list_values[4],vehicle_speed=send_list_values[5])

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

@app.route('/checkhealth')
def checkhealth():
    list1=get_health_values_from_file()
    res=myfunc(list1[1],list1[2],list1[3])
    return render_template('userhomepage.html',res=res)


if __name__ == '__main__':
    app.run(debug=True)