
from flask import Flask, request,flash, jsonify,render_template,session,redirect,url_for
import flask
import json
import os
from datetime import datetime
import re


app=flask.Flask(__name__)




app.secret_key = 'asdfghjkl' 
# IdPatient=0
# UserClass = None
# patient = None
# idpatient=0
# number_appointment=0
class Patient:
    def __init__(self,name, age,date, time):
        self.name=name
        self.age=age
        self.date=date
        self.time=time

class Doctor:
    def __init__(self, doctor_id, name,specialization):
        self.doctor_id = doctor_id  
        self.name = name 
        self.specialization=specialization            

    
    def get_doctor_id(self):
        return self.doctor_id

    
    def set_doctor_id(self, doctor_id):
        self.doctor_id = doctor_id

    def set_doctor_specialization(self, specialization):
        self.specialization = specialization

    
    def get_specialization(self):
        return self.specialization

    
    def get_name(self):
        return self.name

    
    def set_name(self, name):
        self.name = name

class Users:
    def __init__(self,idpatient,name_user,password):
        self.idpatient=idpatient
        self.name_user=name_user
        
        self.password=password

    def getid(self):
        return self.idpatient
    
    def getname(self):
      return self.name_user

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
                return json.load(f) 
            except json.JSONDecodeError:
                return []  
    else:
        return [] 




@app.route('/')
def homepage():
    
    doctors = getdoctors()  
    username = session.get('username')  # Get the username from session
    IdPatient = session.get('IdPatient')  # Get the patient ID from session

    return render_template('home.html', doctors=doctors, username=username, IdPatient=IdPatient)








@app.route("/signup")
def signup_page():
    return render_template("signup.html")





@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form  
        username = data.get('username_sign')
        email = data.get('email_signup')
        password = data.get('password_signup')
        confirm = data.get('password_conform')
        
        if os.path.exists('static/users.json'):
            with open('static/users.json', 'r') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
        else:
            users = []
            
        # Check if users is a list
        if not isinstance(users, list):
            users = []

        # Generate a new patient ID safely
        idPatient = max((user.get('idPatient', 0) for user in users), default=0) + 1
        
        # Validate input fields
        if not all([username, email, password, confirm]):
            flash('Please fill in all fields.', 'error')
            return render_template("signup.html")
        
        # Check for existing email
        if any(user['email'] == email for user in users):
            flash('Email already exists!', 'error')
            return render_template("signup.html")
            
        # Validate password
        if password != confirm:
            flash('Passwords do not match!', 'error')
            return render_template("signup.html")
            
        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return render_template("signup.html")
        if not re.search(r"[A-Z]", password):
            flash('Password must contain at least one uppercase letter.', 'error')
            return render_template("signup.html")
        if not re.search(r"[a-z]", password):
            flash("Password must contain at least one lowercase letter.", 'error')
            return render_template("signup.html")
        if not re.search(r"[0-9]", password):
            flash("Password must contain at least one digit.", 'error')
            return render_template("signup.html")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            flash("Password must contain at least one special character.", 'error')
            return render_template("signup.html")

        # Create new user
        new_user = {
            'idPatient': idPatient,
            'username': username,
            'email': email,
            'password': password
        }
        
        users.append(new_user)

        # Save to file
        try:
            with open('static/users.json', 'w') as f:
                json.dump(users, f, indent=4)
            flash('Sign up successful!', 'success')
            return redirect(url_for('login')) 
        except Exception as e:
            flash('An error occurred during registration.', 'error')
            return render_template("signup.html")

    return render_template("signup.html")


@app.route("/login")
def login():

    return render_template('login.html') 

@app.route("/home", methods=['GET', 'POST'])
def home():
    print(session.get("IdPatient"))
    if request.method == 'POST':
                username = request.form.get("username_login")
                password = request.form.get("password_login")

                users = getjson("users")

                
                
                if not username or not password:
                    flash('Both username and password are required.', 'error')
                    return render_template("login.html") 

                for user in users:
                    if user['username'] == username and user['password'] == password:
                        session["IdPatient"] = user['idPatient']
                        session["username"]=user["username"]
                        session["password"]=user['password']
                        flash('Login successful!', 'success')
                        
                        doctors = getdoctors()  
                        return render_template("home.html", username=username, IdPatient=user['idPatient'], doctors=doctors)

                flash('Invalid username or password. Please try again.', 'error')
                return render_template('login.html')
        
    else:
        print(session["IdPatient"])

        username = session.get("username")  
        doctors = getdoctors() 
        print(username) 
        return render_template("home.html", username=username, IdPatient=session["IdPatient"], doctors=doctors)
    




@app.route("/logout")
def logout():
  session.clear()
  doctors = getdoctors() 
  return render_template("home.html",doctors=doctors)

            

         
    

   
@app.route("/about")
def about():
    return render_template("about.html")


#get booking page
@app.route("/booking")
def booking():
    doctor_name = request.args.get('doctor_name')
    doctor_id = request.args.get('doctor_id')
    doctor_specialization = request.args.get('doctor_specialization')
    doctor=Doctor(doctor_id,doctor_name,doctor_specialization)
    
    return render_template("booking.html" , doctor_name=doctor.get_name(),specialization=doctor.get_specialization())  


@app.route("/booking", methods=['POST'])
def appointment():
    global IdPatient
    global number_appointment
    

    if request.method == 'POST':
        data = request.get_json()
        
        
        # Extract patient details from the JSON request
        IdPatient=data.get("IdPatient")
        name_doctor=data.get("doctorName")
        specialization=data.get("doctor_specialization")
        name_patient = data.get("name_patient")
        age_patient = data.get("age_patient")
        Date = data.get("Date")
        Time = data.get("Time")


        #set idpatient in session 
        session['IdPatient'] = IdPatient

        # Validate input data
        if not name_patient or not isinstance(name_patient, str):
            return jsonify(message='Invalid name provided; must be a string'), 400

        if not isinstance(age_patient, str) or not age_patient.isnumeric():
            return jsonify(message='Invalid age provided; must be a number'), 400
        
        # Load existing appointments from JSON file
        with open('static/appointment.json', 'r') as f:
            try:
                appointments = json.load(f)
            except json.JSONDecodeError:
                appointments = []  # Handle JSON decoding errors

        # Determine the next appointment number
        number_appointment = max((num.get('NumberAppointment', 0) for patient in appointments for num in patient.get('appointments', [])), default=0) + 1

        # Create new appointment record
        new_appointment = {
            "NumberAppointment": number_appointment,
            "name_doctor": name_doctor,
            "specialization":specialization,
            "name_patient": name_patient,
            "age_patient": int(age_patient),  # Convert to integer
            "Date": {
                "day": Date["day"],
                "month": Date["month"],
                "year": Date["year"],
            },
            "Time": {
                "Hour": Time["Hour"],
                "Minute": Time["Minute"]
            }
        }

        
        patient_found = False
        for patient_record in appointments:
            if patient_record["IdPatient"] == IdPatient:
                patient_found = True
                if "appointments" not in patient_record:
                    patient_record["appointments"] = [] 
                patient_record["appointments"].append(new_appointment)
                break
        
        
        if not patient_found:
            new_patient_record = {
                "IdPatient": IdPatient,
                "appointments": [new_appointment]
            }
            appointments.append(new_patient_record)

        
        with open('static/appointment.json', 'w') as f:
            json.dump(appointments, f, indent=4)

        return jsonify(message='Appointment created successfully', appointment=new_appointment), 201

# this function to veiw_booking to post and get data from to javascritp to rout 
@app.route('/veiw_booking', methods=['POST', 'GET'])
def veiw_booking():
    global UserClass
    global patient
    global IdPatient
    global user

    if request.method == 'POST':
        data = request.get_json()
        print(data)
        
        NewName = data['namePatient']
        NewAge = data['agePatient']
        NewDate = data['appointmentDate']     
        NewTime = data['appointmentTime']  
 
        NewDate = datetime.strptime(NewDate, '%Y-%m-%d')
        NewTime = datetime.strptime(NewTime, '%H:%M:%S')  
        print(NewAge)          
                                
        with open('static/appointment.json', 'r') as f:
            appointments = json.load(f)
            
        number_appointment = max((num.get('NumberAppointment', 0) for patient in appointments for num in patient.get('appointments', [])), default=0) + 1
        
        new_appointment_view = {
            "NumberAppointment": number_appointment,
            "name_patient": NewName,
            "age_patient": NewAge,
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
        print(new_appointment_view)

        # Find the patient by IdPatient and append the new appointment
        patient_found = False
        for patient_record in appointments:
            if patient_record["IdPatient"] == IdPatient:
                patient_found = True
                if "appointments" not in patient_record:
                    patient_record["appointments"] = [] 
                patient_record["appointments"].append(new_appointment_view)
                break
        
        # If the patient was not found, create a new record
        if not patient_found:
            new_patient_record = {
                "IdPatient": IdPatient,
                "appointments": [new_appointment_view]
            }
            appointments.append(new_patient_record)
               
        # Write the updated list back to the file
        with open('static/appointment.json', 'w') as f:
            json.dump(appointments, f, indent=2)

        return jsonify({
            "message": "New appointment recorded successfully",
            "IdPatient": IdPatient,
            "numberapp": number_appointment,
            "status": 200
        })

    # Handle GET request
    elif request.method == 'GET':
        
        IdPatient = session.get('IdPatient')
        try:
            with open('static/appointment.json', 'r') as f:
                appointments_data = json.load(f)
            
            # Find appointments for the current patient
            patient_appointments = []
            for patient_record in appointments_data:
                if patient_record["IdPatient"] == IdPatient:
                    patient_appointments = patient_record["appointments"]
                   
                    break
            
            # Render template with all appointments for the current patient
            return render_template(
                "veiw_booking.html",
                appointments=patient_appointments,
                IdPatient=IdPatient
            )
            
        except FileNotFoundError:
            print("Appointment file not found")
            return render_template(
                "veiw_booking.html",
                appointments=[],
                IdPatient=IdPatient
            )
        except json.JSONDecodeError:
            print("Error decoding appointment file")
            return render_template(
                "veiw_booking.html",
                appointments=[],
                IdPatient=IdPatient
            )
        except Exception as e:
            print(f"Unexpected error: {e}")
            return render_template(
                "veiw_booking.html",
                appointments=[],
                IdPatient=IdPatient
            )

#delete 
@app.route('/delete' , methods=["DELETE"])
def delete():
    dataDelete=request.get_json()
    IdPatient=dataDelete.get("IdPatient")
    appointmentId=dataDelete.get("appointmentId")
    with open('static/appointment.json', 'r') as f:
       appointments_data = json.load(f)


    # Find the patient and delete the appointment
    for patient in appointments_data:
        if int(patient["IdPatient"]) == int(IdPatient):  
            patient["appointments"] = [
                appointment for appointment in patient["appointments"]
                if int(appointment["NumberAppointment"]) != int(appointmentId)
            ]
    with open('static/appointment.json', 'w') as f:
        json.dump(appointments_data, f, indent=4)

    return {"message": "Appointment deleted successfully."}, 200




@app.route('/update', methods=["POST"])
def update():
    dataUpdate=request.get_json()
    IdPatient=dataUpdate.get("IdPatient")
    appointmentId=dataUpdate.get("appointmentId")
    date=dataUpdate.get("date")
    time=dataUpdate.get("time")
    dateobj = datetime.strptime(date, '%Y-%m-%d')
    Timeobj = datetime.strptime(time, '%H:%M')  
    day=dateobj.day
    month=dateobj.month
    year=dateobj.year
    Hour=Timeobj.hour
    Minute=Timeobj.minute


    # Load the JSON data
    with open('static/appointment.json', 'r') as f:
        appointments_data = json.load(f)

    for patient in appointments_data:
        

        if int(patient["IdPatient"] )== int(IdPatient):
            
            for appointment in patient["appointments"]:
                if int(appointment["NumberAppointment"]) == int(appointmentId):
                    
                    
                    appointment["Date"]["day"] = day
                    appointment["Date"]["month"] = month
                    appointment["Date"]["year"] = year
                    appointment["Time"]["Hour"] = Hour
                    appointment["Time"]["Minute"] = Minute

                
    with open('static/appointment.json', 'w') as f:
        json.dump(appointments_data, f, indent=4)
        
    return jsonify(message='Appointment updated successfully'), 201






if __name__ == "__main__":
        
    app.run(debug=True)



