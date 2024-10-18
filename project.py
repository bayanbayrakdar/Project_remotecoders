
from flask import Flask, request, jsonify, render_template
import flask
import json
import os

app=flask.Flask(__name__)

   
@app.route("/about")
def about():
    return render_template("about.html")


#get booking page
@app.route("/booking")
def booking():
    return render_template("booking.html")  


@app.route("/booking", methods=['POST'])
def appointment():
    if request.method == 'POST':
        data = request.get_json()
        print(data) 

        # Extract and validate data
        name_patient = data.get("name_patient")
        age_patient = data.get("age_patient")

        patient=patient(name_patient,age_patient)

        if not name_patient or not isinstance(name_patient, str):
            return jsonify(message='Invalid name provided; must be a number'), 400

        if not isinstance(age_patient, str) or not age_patient.isnumeric():
            return jsonify(message='Invalid age provided; must be a number'), 400

        # Create a new appointment record
        new_appointment = {
            "name_patient": name_patient,
            "age_patient": int(age_patient)  # Convert to integer
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
    return render_template("veiw_booking.html")

@app.route('/veiw_booking',methods=['GET', 'POST'])
def veiw_booking1():

    with open("oppointment.json" , 'r') as file:

        data=json.load(file)
    print(data)







if __name__ == "__main__":
    app.run(debug=True)



