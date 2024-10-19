
from flask import Flask, request, jsonify, render_template
import flask
import json
import os

#save booking info to json file
import os
import json

app=flask.Flask(__name__)
Data_user = None
patient = None
class Patient:
    def __init__(self,name, age,date, time):
        self.name=name
        self.age=age
        self.date=date
        self.time=time

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
    





   
@app.route("/about")
def about():
    return render_template("about.html")


#get booking page
@app.route("/booking")
def booking():
    return render_template("booking.html")  


@app.route("/booking", methods=['POST'])
def appointment():
    global patient
    if request.method == 'POST':
        data = request.get_json()
        

        # Extract and validate data
        name_patient = data.get("name_patient")
        age_patient = data.get("age_patient")
        Date= data.get("Date")
        Time=data.get("Time")

        print(Time["Hour"])
        
        

        patient=Patient(name_patient,age_patient,Date,Time)
        

        if not name_patient or not isinstance(name_patient, str):
            return jsonify(message='Invalid name provided; must be a number'), 400

        if not isinstance(age_patient, str) or not age_patient.isnumeric():
            return jsonify(message='Invalid age provided; must be a number'), 400

        # Create a new appointment record
        new_appointment = {
            "name_patient": name_patient,
            "age_patient": int(age_patient) , # Convert to integer
            "Date":{
                "day":Date["day"],
                "month":Date["month"],
                "year":Date["year"],
            },
            "Time" : {
                "Hour" : Time["Hour"],
                "Minute" : Time["Minute"]
            }
        }

        # Load existing appointments or create a new list
        if os.path.exists('appointment.json'):
            with open('appointment.json', 'r') as f:
                try:
                    appointments = json.load(f)
                except json.JSONDecodeError:
                    appointments = []  # Handle JSON decoding errors
        else:
            appointments = []

        # Append the new appointment to the list
        appointments.append(new_appointment)

        # Write the updated list back to the file
        with open('appointment.json', 'w') as f:
            json.dump(appointments, f, indent=2)
    
    
    return jsonify(message='Appointment successfully created'),200






@app.route('/veiw_booking')
def veiw_booking():

    global patient

    return render_template("veiw_booking.html", name_patient=patient.name if patient else " ", age_patient=patient.age if patient else " " , 
                           Date=f"{patient.date['day']}/{patient.date['month']}/{patient.date['year']}" if patient else " " , Time=f"{patient.time['Hour']}:{patient.time['Minute']}" if patient else " " , id=123)


# @app.route('/veiw_booking',methods=['GET', 'POST','DELETE','PUT'])
# def Edit_booking():
#     if methods==['DELETE']:




#     with open("oppointment.json" , 'r') as file:

#         data=json.load(file)
#     print(data)







if __name__ == "__main__":
    
    app.run(debug=True)



