
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
IdPatient=0
UserClass = None
patient = None
idpatient=0
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


def getdoctors():
    with open("static/doctors.json") as f:
        return json.load(f)

def getjson(file):
    # Load existing data or create a new list
    file_path = 'static/' + file + '.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                return json.load(f)  # Return loaded JSON data
            except json.JSONDecodeError:
                return []  # Return empty list if JSON is invalid
    else:
        return []  # Return empty list if file doesn't exist



@app.route("/")
def home1():
    doctors=getdoctors()
    
    return render_template("home.html",doctors=doctors)

def authenticate(username, password):
    # Dummy authentication logic (replace with your own)
    return username == "admin" and password == "password"

@app.route("/login", methods=['POST' ,'GET'])
def login():

    return render_template('login.html') 


@app.route("/home", methods=['GET', 'POST'])
def home():
    global IdPatient
    if request.method == 'POST':
        
        username = request.form.get("username_login")
        password = request.form.get("password_login")

        users = getjson("users")  # Assuming this function returns a list of user dictionaries

        # Check if username and password are provided
        if not username or not password:
            flash('Both username and password are required.', 'error')
            return render_template("login.html") 
            



        for user in users:

                

            if user['username'] == username and user['password'] == password:
                
                IdPatient=user['idPatient']
                # print(IdPatient)
                print("hsjj")
                flash('Login successful!', 'success')
                return render_template("home.html" ,username=username ,IdPatient=IdPatient)  # Redirect on successful login


 
    flash('Invalid username or password. Please try again.', 'error')
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
    
    # Load existing users from JSON file
    if os.path.exists('static/users.json'):
        with open('static/users.json', 'r') as f:
            users = json.load(f)
    else:
        users = []

    # Generate a new patient ID safely
    idPatient = max((user.get('idPatient', 0) for user in users), default=0) + 1

    # Validate input fields
    if not all([username, email, password, confirm]):
        return jsonify(message='Please fill in all fields.'), 400

    if password != confirm:
        return jsonify(message='Passwords do not match!'), 400

    if any(user['username'] == username for user in users):
        return jsonify(message='Username already exists!'), 400

    # Create user data and save to JSON
    user_data = {
        "idPatient": idPatient,
        "username": username,
        "email": email,
        "password": password
    }
    users.append(user_data)
    UserClass = Users(idPatient, username, email, password)
    # print(UserClass.getid())

    with open('static/users.json', 'w') as f:
        json.dump(users, f, indent=2)

    # print(idPatient)
    jsonify(message='SignUp successful!'), 201
    # Instead of flash, return a success message
    return render_template("home.html")



   
@app.route("/about")
def about():
    return render_template("about.html")


#get booking page
@app.route("/booking")
def booking():
    
    return render_template("booking.html")  


@app.route("/booking", methods=['POST'])
def appointment():
    global IdPatient
    global patient
    global UserClass
    global idpatient
    global username
    
    if request.method == 'POST':
        data = request.get_json()
        username = request.form.get("username_login")
        password = request.form.get("password_login")
        data_username=request.json
        username=data.get("username")
        

        # Extract and validate data
        name_patient = data.get("name_patient")
        age_patient = data.get("age_patient")
        Date= data.get("Date")
        Time=data.get("Time")
        # print(IdPatient)

        # extract user
        # Users = getjson("users") 
        # for user in Users:

        #     username= user['username']
        #     idpatient=user['idPatient']


        
        

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
        new_appointmentuser ={
            
            "IdPatient":IdPatient,
            "appointment" :new_appointment,
        }
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
        appointments.append(new_appointmentuser)

        # Write the updated list back to the file
        with open('static/appointment.json', 'w') as f:
            json.dump(appointments, f, indent=2)
    

    
    return jsonify(message='Appointment successfully created'),200


@app.route('/veiw_booking', methods=['POST', 'GET'])
def veiw_booking():
    global UserClass
    global patient
    global IdPatient

    if request.method == 'POST':
        NewName = request.form.get("patientname")
        NewAge = request.form.get("patientage")
        datePatient = request.form.get("date")

        try:
            datePatient = datetime.strptime(datePatient, '%Y-%m-%dT%H:%M')
            NewDate = datePatient.date()
            NewTime = datePatient.time()
        except (ValueError, TypeError):
            flash('Invalid date format. Please use the correct format.', 'error')
            return render_template("booking.html")

        new_appointment_view = {
            "name_patient": NewName,
            "age_patient": int(NewAge),
            "Date": {
                "day": NewDate.day,
                "month": NewDate.month,
                "year": NewDate.year,
            },
            "Time": {
                "Hour": NewTime.hour,
                "Minute": NewTime.minute
            }
        }

        print("New appointment view:", new_appointment_view)

        appointments = getjson("appointment")

        # Find the specific patient by IdPatient
        patient_found = False
        for appointment in appointments:
            if appointment["IdPatient"] == IdPatient:
                patient_found = True
                # Check if appointments list exists, if not create one
                if "appointments" not in appointment:
                    appointment["appointments"] = []
                # Append the new appointment to the patient's appointments list
                appointment["appointments"].append(new_appointment_view)
                print("New appointment added under IdPatient:", IdPatient)
                break

        if not patient_found:
            # If no existing patient, create a new entry
            appointments.append({
                "IdPatient": IdPatient,
                "appointments": [new_appointment_view]
            })
            print("New patient added with IdPatient:", IdPatient)

        # Save updated appointments back to the JSON file
        with open('static/appointment.json', 'w') as f:
            json.dump(appointments, f)

        # Create new patient object
        newpatient = Patient(NewName, NewAge, NewDate, NewTime)

        return render_template("veiw_booking.html", 
                               name_patient=newpatient.name, 
                               age_patient=newpatient.age, 
                               Date=f"{NewDate.day}/{NewDate.month}/{NewDate.year}", 
                               Time=f"{NewTime.hour}:{NewTime.minute}", 
                               id=IdPatient)

    # Handle GET request and render existing patient information
    return render_template("veiw_booking.html", 
                           name_patient=patient.name if patient else " ", 
                           age_patient=patient.age if patient else " ", 
                           Date=f"{patient.date['day']}/{patient.date['month']}/{patient.date['year']}" if patient else " ", 
                           Time=f"{patient.time['Hour']}:{patient.time['Minute']}" if patient else " ", 
                           id=IdPatient)






# @app.route('/veiw_booking',methods=['GET', 'POST','DELETE','PUT'])
# def Edit_booking():
#     if methods==['DELETE']:




#     with open("oppointment.json" , 'r') as file:

#         data=json.load(file)
#     print(data)







if __name__ == "__main__":
    
    app.run(debug=True)



