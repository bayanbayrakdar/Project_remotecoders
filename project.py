
from flask import Flask, request,flash,url_for, jsonify, redirect,render_template
import flask
import json
import os
from datetime import datetime
import bcrypt



#save booking info to json file
import os
import json

app=flask.Flask(__name__)

app.secret_key = 'asdfghjkl'  # Set this to a random string
id_patient=0
UserClass = None
patient = None
class Patient:
    def __init__(self,name, age,date, time):
        self.name=name
        self.age=age
        self.date=date
        self.time=time

class Users:
    def __init__(self,idpatient,name_user,email,password):
        self.idpatient=idpatient
        self.name_user=name_user
        self.email=email
        self.password=password

    def getid(self):
        return self.idpatient
    
    def getname(self):
      return self.name_user
    def getemail(self):
      return self.email
    def getpassword(self):
        return self.password




def getjson(file):

        # Load existing users or create a new list
    if os.path.exists('static/'+file+'.json'):
        with open('static/'+file+'.json', 'r') as f:
            fileJson = json.load(f)
    else:
            fileJson = jsonify(message="No user find"), 404

    return fileJson



@app.route("/")
def home1():
    
    return render_template("home.html")

def authenticate(username, password):
    # Dummy authentication logic (replace with your own)
    return username == "admin" and password == "password"

@app.route("/login", methods=['POST' ,'GET'])
def login():

    return render_template('login.html') 


@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get("username_login")
        password = request.form.get("password_login")

        users = getjson("users")  # Assuming this function returns a list of user dictionaries

        # Check if username and password are provided
        if not username or not password:
            flash('Both username and password are required.', 'error')
            return render_template("login.html") 
            



        for user in users:
            if user['username'] == username or user['password'] == password:

                flash('Login successful!', 'success')
                return render_template("home.html")  # Redirect on successful login
            else:
                flash('Invalid username or password. Please try again.', 'error')
                return render_template("login.html")  # Redirect if password is incorrect



    return render_template('login.html')


@app.route("/signup")
def signup_page():
    return render_template("signup.html")



@app.route('/signup', methods=['POST'])
def signup():
    global UserClass 
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm = data.get('confirm')
    
    if os.path.exists('static/users.json'):
        with open('static/users.json', 'r') as f:
            users = json.load(f)
    else:
        users = []

        # Generate a new patient ID safely
    if users:  # Check if users list is not empty
        idPatient = max(user.get('idPatient', 0) for user in users) + 1
    else:
        idPatient = 1  # Start from 1 if no users exist


    print("ss")

    if username and email and password and confirm:
        if password != confirm:
            return jsonify(message='Passwords do not match!'), 400
        if any(user['username'] == username for user in users):
            return jsonify(message='Username already exists!'), 400
        

        

        
        user_data = {
            "idPatient":idPatient,
            
            'username': username,
            'email': email,
            'password': password
        }
        users.append(user_data)
        UserClass=Users(idPatient,username,email,password)

        with open('static/users.json', 'w') as f:
            json.dump(users, f, indent=2)

        return jsonify(message='User registered successfully!'), 201
    
    return jsonify(message='Please fill in all fields.'), 400
   
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
    global UserClass
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
        print(UserClass.getid())

        # Load existing appointments or create a new list
        if os.path.exists('static/appointment.json'):
            with open('static/appointment.json', 'r') as f:
                try:
                    appointments = json.load(f)
                except json.JSONDecodeError:
                    appointments = []  # Handle JSON decoding errors
        else:
            appointments = []

        # Append the new appointment to the list
        appointments.append(new_appointment)

        # Write the updated list back to the file
        with open('static/appointment.json', 'w') as f:
            json.dump(appointments, f, indent=2)
    
    
    return jsonify(message='Appointment successfully created'),200






@app.route('/veiw_booking', methods=['POST', 'GET'])
def veiw_booking():
    global UserClass

    global patient

    if request.method == 'POST':
        NewName=request.form.get("patientname")
        NewAge=request.form.get("patientage")
        datePatient=request.form.get("date")
        datePatient=datetime.strptime(datePatient, '%Y-%m-%dT%H:%M')
        NewDate=datePatient.date()
        NewTime=datePatient.time()
        

        newpatient=Patient(NewName,NewAge,NewDate,NewTime)
        

        return render_template("veiw_booking.html", name_patient=newpatient.name if patient else " ", age_patient=newpatient.age if patient else " " , 
                           Date=newpatient.date if patient else " " , Time=newpatient.time if patient else " " , id=UserClass.getid())




    return render_template("veiw_booking.html", name_patient=patient.name if patient else " ", age_patient=patient.age if patient else " " , 
                           Date=f"{patient.date['day']}/{patient.date['month']}/{patient.date['year']}" if patient else " " , Time=f"{patient.time['Hour']}:{patient.time['Minute']}" if patient else " " , id=UserClass.getid())


# @app.route('/veiw_booking',methods=['GET', 'POST','DELETE','PUT'])
# def Edit_booking():
#     if methods==['DELETE']:




#     with open("oppointment.json" , 'r') as file:

#         data=json.load(file)
#     print(data)







if __name__ == "__main__":
    
    app.run(debug=True)



