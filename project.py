
from flask import Flask, request,flash,url_for, jsonify, redirect,render_template,session
import flask
import json
import os
from datetime import datetime
import bcrypt



#save booking info to json file
import os
import json

app=flask.Flask(__name__)


# def setup_appointment_routes(app):
#     @app.route('/veiw_booking/<int:appointment_number>', methods=['DELETE'])
#     def delete_appointment(appointment_number):
#         try:
#             with open('static/appointment.json', 'r') as f:
#                 appointments = json.load(f)

#             # Find and remove the appointment
#             for patient in appointments:
#                 patient['appointments'] = [
#                     appt for appt in patient.get('appointments', [])
#                     if appt['NumberAppointment'] != appointment_number
#                 ]

#             # Save updated appointments
#             with open('static/appointment.json', 'w') as f:
#                 json.dump(appointments, f, indent=2)

#             return jsonify({'message': 'Appointment deleted successfully'}), 200
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

#     @app.route('/veiw_booking/<int:appointment_number>', methods=['PUT'])
#     def update_appointment(appointment_number):
#         try:
#             data = request.json
#             with open('static/appointment.json', 'r') as f:
#                 appointments = json.load(f)

#             # Update the appointment
#             appointment_found = False
#             for patient in appointments:
#                 for appointment in patient.get('appointments', []):
#                     if appointment['NumberAppointment'] == appointment_number:
#                         # Update appointment details
#                         appointment['name_patient'] = data['patientName']
#                         appointment['age_patient'] = int(data['patientAge'])
                        
#                         # Parse and update date
#                         date_parts = data['date'].split()
#                         appointment['Date'] = {
#                             'day': int(date_parts[0]),
#                             'month': date_parts[1].rstrip(','),
#                             'year': int(date_parts[2])
#                         }
                        
#                         # Parse and update time
#                         time_parts = data['time'].split(':')
#                         appointment['Time'] = {
#                             'Hour': int(time_parts[0]),
#                             'Minute': int(time_parts[1])
#                         }
                        
#                         appointment_found = True
#                         break
#                 if appointment_found:
#                     break

#             if not appointment_found:
#                 return jsonify({'error': 'Appointment not found'}), 404

#             # Save updated appointments
#             with open('static/appointment.json', 'w') as f:
#                 json.dump(appointments, f, indent=2)

#             return jsonify({'message': 'Appointment updated successfully'}), 200
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

#     @app.template_filter('format_date')
#     def format_date(date_dict):
#         """Format date dictionary into a readable string"""
#         try:
#             return f"{date_dict['day']} {date_dict['month']}, {date_dict['year']}"
#         except:
#             return "Invalid date"

#     @app.template_filter('format_time')
#     def format_time(time_dict):
#         """Format time dictionary into a readable string"""
#         try:
#             return f"{time_dict['Hour']:02d}:{time_dict['Minute']:02d}"
#         except:
#             return "Invalid time"


app.secret_key = 'asdfghjkl'  # Set this to a random string
IdPatient=0
UserClass = None
patient = None
idpatient=0
number_appointment=0
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




@app.route('/')
def home1():
    # Assume you have a function to get the list of doctors
    doctors = getdoctors()  # This should return a list of doctors
    username = session.get('username')  # Get the username from session
    IdPatient = session.get('IdPatient')  # Get the patient ID from session

    return render_template('home.html', doctors=doctors, username=username, IdPatient=IdPatient)

    
   

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

        if not username or not password:
            flash('Both username and password are required.', 'error')
            return render_template("login.html") 

        for user in users:
            if user['username'] == username and user['password'] == password:
                IdPatient = user['idPatient']
                flash('Login successful!', 'success')

                # Fetch doctors
                doctors = getdoctors()  # Fetch the list of doctors here

                return render_template("home.html", username=username, IdPatient=IdPatient, doctors=doctors)  # Pass doctors to template

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
    global number_appointment

    if request.method == 'POST':
        data = request.get_json()
        
        # Extract patient details from the JSON request
        name_patient = data.get("name_patient")
        age_patient = data.get("age_patient")
        Date = data.get("Date")
        Time = data.get("Time")

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

        # Find the patient by IdPatient and append the new appointment
        patient_found = False
        for patient_record in appointments:
            if patient_record["IdPatient"] == IdPatient:
                patient_found = True
                if "appointments" not in patient_record:
                    patient_record["appointments"] = [] 
                patient_record["appointments"].append(new_appointment)
                break
        
        # If the patient was not found, create a new record
        if not patient_found:
            new_patient_record = {
                "IdPatient": IdPatient,
                "appointments": [new_appointment]
            }
            appointments.append(new_patient_record)

        # Save the updated appointments back to the JSON file
        with open('static/appointment.json', 'w') as f:
            json.dump(appointments, f, indent=4)

        return jsonify(message='Appointment created successfully', appointment=new_appointment), 201


# @app.route('/veiw_booking',methods=['DELETE'])
# def delete():


@app.route('/veiw_booking', methods=['POST', 'GET'])
def veiw_booking():
    global UserClass
    global patient
    global IdPatient

    if request.method == 'POST':
        data = request.get_json()
        
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
            "numberapp": number_appointment,
            "status": 200
        })

    # Handle GET request
    elif request.method == 'GET':
        try:
            with open('static/appointment.json', 'r') as f:
                appointments_data = json.load(f)
            
            # Find appointments for the current patient
            patient_appointments = []
            for patient_record in appointments_data:
                if patient_record["IdPatient"] == IdPatient:
                    patient_appointments = patient_record.get("appointments", [])
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
 




# @app.route('/view_booking', methods=['GET', 'POST'])
# def appentTable():
#     global IdPatient
#     all_appointment = []
    

#     # Load appointments from the JSON file
#     with open("static/appointment.json", 'r') as f:
#         appointment_table = json.load(f)

#     # Loop through each patient record to find matching IdPatient
#     for patient_record in appointment_table:
#         if patient_record["IdPatient"] == int(IdPatient):
#             all_appointment.extend(patient_record.get("appointments", []))

#     # Prepare to return to template
#     if all_appointment:
#         # Use the last appointment (or however you want to display them)
#         last_appointment = all_appointment[-1]  # Get the last appointment or process as needed
#         numberAppointment = last_appointment['NumberAppointment']
#         namePatient = last_appointment['name_patient']
#         agePatient = last_appointment['age_patient']
#         day = last_appointment['Date']['day']
#         month = last_appointment['Date']['month']
#         year = last_appointment['Date']['year']
#         hour = last_appointment['Time']['Hour']
#         minute = last_appointment['Time']['Minute']

#         return render_template("veiw_booking.html",
#                                id=IdPatient,
#                                numberAppointment=numberAppointment,
#                                name_patient=namePatient,
#                                age_patient=agePatient,
#                                Date=f"{day}/{month}/{year}",
#                                Time=f"{hour}:{minute}")
#     else:
#         return render_template("veiw_booking.html", id=IdPatient, message="No appointments found.")




# @app.route('/veiw_booking',methods=['GET', 'POST','DELETE','PUT'])
# def Edit_booking():
#     if methods==['DELETE']:




#     with open("oppointment.json" , 'r') as file:

#         data=json.load(file)
#     print(data)






if __name__ == "__main__":
    

    # all_appointment=[]
    
    # with open("static/appointment.json", 'r') as f:           
    #     appointment_table= json.load(f)  # Return loaded JSON data


    # for patient_record in appointment_table:
    #     if patient_record["IdPatient"] == IdPatient:              
    #        all_appointment.append(patient_record["appointments"])
        
    # print(all_appointment)
        
    # # Write the updated list back to the file
    # with open('static/newappointment.json', 'w') as f:
    #     json.dump(all_appointment, f, indent=2)
    
    
    app.run(debug=True)



