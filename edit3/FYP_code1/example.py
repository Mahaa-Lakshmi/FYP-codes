import requests
from firebase import firebase
from flask import Flask,render_template,request
app = Flask(__name__)

firebase=firebase.FirebaseApplication("https://svhms-user-details-default-rtdb.firebaseio.com/",None)

@app.route("/")
def home():
  result = firebase.get('/users',None)
  result=list(filter(None, result))
  print(result)
  return render_template("example.html",users=result)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
  if request.method == 'POST' and len(dict(request.form)) > 0:
    userdata = dict(request.form)
    email = userdata["email"]
    car = userdata["car"]
    model = userdata["model"]
    password = userdata["password"]
    new_data = {"email": email, "car": car,"model":model,"password":password}
    new_data={'3':new_data}
    firebase.post("/users", new_data)
    return "Thank you!"
  else:
    return "Sorry, there was an error."

if __name__ == '__main__':
    app.run(debug=True)

'''
data={
    'Name':'Mahaa',
    'Email':'bmaha4@gmail.com',
    'phone':'123456789'

}

result=firebase.post('/svhms-user-details-default-rtdb/3',data)
print(result)
'''