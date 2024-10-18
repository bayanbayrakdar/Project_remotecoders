from flask import Flask, request, jsonify, render_template
import flask
import json
import os

app=flask.Flask(__name__)
global Data_user
global patient
class patient:
    def __init__(self,id_patient,name_patient,age_patiennt,date,hour) -> None:
        self.id_patient=id_patient
        self.name_patient=name_patient
        self.age_patiennt=age_patiennt
        self.date=date
        self.hour=hour

        pass

class users:
    def __init__(self,name_user,email,password):
        self.name_user=name_user
        self.email=email
        self.password=password


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login_page():
        return render_template("login.html")

@app.route("/login" , methods=['POST'])
def login():
    data=request.get_json()

    username=data.get("username")
    password=data.get("password")
    user_data={"username": username ,"password": password}

    # Load existing users or create a new list
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            user_data = json.load(f)
    else:
            user_data = jsonify(message="No user find"), 404


    for user in user_data:
            if user['username'] == username and user['password'] == password:  # Use hashed password check in production
                return jsonify(message='Login successful!', success=True), 200
            
            
    return jsonify(message='Invalid username or password.', success=False), 401


@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def signup():
    # Get the JSON data from the request
 
    data = request.get_json()
    


    # chech if user exict 
    username = data.get('username')
    email = data.get('email')
    password = data.get('password') 
    confirm=data.get('confirm')

    # Prepare the user data
    user_data = {
        "username": username,
        "email": email,
        "password": password ,
        "confim":confirm
    }

    

    # Data_user=users(username,email,password)

    
    if confirm!=password:
        return jsonify(message='Passwords do not match!'), 400
    
    if not username and not email  and not password  and not confirm :
        jsonify(message='must fill all ')


    # Load existing users or create a new list
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            users = json.load(f)
    else:
        users = []

    # Append new user data
    users.append(user_data)

    # Write back to the JSON file
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

    return jsonify(message='User registered successfully!')
    


if __name__ == "__main__":
    app.run(debug=True)

