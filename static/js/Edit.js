// Update your existing addRow function to handle the JSON structure
function addRow(event) {
    event.preventDefault();

    // Get input elements
    const namePatient = document.getElementById('name_patient');
    const agePatient = document.getElementById('age_patient');
    const table = document.getElementById('outputTable').getElementsByTagName('tbody')[0];

    // Get data from localStorage
    const newdata = localStorage.getItem("newdata");
    const newtime = localStorage.getItem("newtime");

    // Create new row
    const newRow = table.insertRow();

    // Insert cells
    const cell1 = newRow.insertCell(0);
    const cell2 = newRow.insertCell(1);
    const cell3 = newRow.insertCell(2);
    const cell4 = newRow.insertCell(3);
    const cell5 = newRow.insertCell(4);
    const cell6 = newRow.insertCell(5);
    const cell7 = newRow.insertCell(6);

    // Create data object matching your JSON structure
    const appointmentData = {
        namePatient: namePatient.value,
        agePatient: agePatient.value,
        appointmentDate: newdata,
        appointmentTime: newtime
    };

    // Set cell contents
    cell1.innerHTML = IdPatient.innerHTML || '';  // Use your existing IdPatient variable
    cell2.innerHTML = '';
    cell3.innerHTML = namePatient.value;
    cell4.innerHTML = agePatient.value;
    cell5.innerHTML = newdata || "No Date";
    cell6.innerHTML = newtime || "No Time";
    cell7.innerHTML = `
        <button class="save">Save</button>
        <button type="button" class="btn btn-success" data-toggle="modal" data-target="#myModal">Edit</button>
        <button class="delete" onclick="removeRow(this)">Delete</button>
    `;

    // Send to server
    fetch('/veiw_booking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(appointmentData)
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            console.log('Success:', data);
            // Update the appointment number after server response
            cell2.innerHTML = data.numberapp;
            window.location.href = "/veiw_booking";
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


// Add this new function to load existing appointments
function loadExistingAppointments() {
    fetch('/static/appointment.json')
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById('outputTable').getElementsByTagName('tbody')[0];

            // Clear existing table rows
            table.innerHTML = '';

            // Loop through each patient
            data.forEach(patient => {
                // Loop through each appointment for this patient
                patient.appointments.forEach(appointment => {
                    const newRow = table.insertRow();

                    // Create cells
                    const cells = [
                        patient.IdPatient,
                        appointment.NumberAppointment,
                        appointment.name_patient,
                        appointment.age_patient,
                        `${appointment.Date.day} ${appointment.Date.month}, ${appointment.Date.year}`,
                        `${appointment.Time.Hour}:${appointment.Time.Minute}`,
                        `<button class="save">Save</button>
                         <button id="buttonEDit" class="btn btn-success" data-toggle="modal" data-target="#myModal" data-id=${appointment.NumberAppointment}>Edit</button>
                         <button class="delete" onclick="removeRow(this)">Delete</button>`
                    ];

                    // Add each cell to the row
                    cells.forEach((content, index) => {
                        const cell = newRow.insertCell(index);
                        cell.innerHTML = content;


                    });
                });
            });
        })
        .catch(error => console.error('Error loading appointments:', error));
}



// Call loadExistingAppointments when the page loads
document.addEventListener('DOMContentLoaded', () => {
    loadExistingAppointments();


    // Your existing event listeners
    const formtable = document.getElementById('booking');
    if (formtable) {
        formtable.addEventListener('submit', addRow);
    } else {
        console.error('Booking form not found');
    }
});
// const cal=document.getElementById("cal")
// console.log(cal.value)
function GetCal(event) {
    event.preventDefault()
    const cal = document.getElementById("caledit")
    console.log(cal.value)


}


//this is for backend to edit 
// document.addEventListener('click', (e) => {
//     if (e.target.getAttribute('id') === 'buttonEDit') {
//         const appointmentId = e.target.getAttribute("data-id");
//         console.log(appointmentId);
//         localStorage.setItem("appointmentId", appointmentId)


//         showModaledit(appointmentId); // Pass appointmentId to the modal if needed
//     }

    // if (e.target.getAttribute('id') === 'confermEdit') {
    //     const dateTimeInput = document.getElementById("caledit").value;
    //     const appointmentId = e.target.getAttribute("data-id");

    //     const formData = new FormData();
    //     formData.append('date', dateTimeInput);
    //     formData.append('appointmentId', appointmentId);

    //     fetch('/submit', {
    //         method: 'POST',
    //         body: formData,
    //     })
    //         .then(response => response.text())
    //         .then(data => {
    //             console.log(data);
    //             alert(data);
    //         })
    //         .catch(error => console.error('Error:', error));
    // }
});









// Your existing removeRow function remains the same
function removeRow(button) {
    const row = button.closest('tr');
    if (row) {
        row.remove();
    }
}

// Your existing modal functions remain the same
function showModal() {
    document.getElementById('modal').style.display = 'block';
    document.getElementById('overlay').classList.add('active');
}
function showModaledit() {
    document.getElementById('modaledit').style.display = 'block';
    document.getElementById('overlay').classList.add('active');
}

function hideModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('overlay').classList.remove('active');
}

function hideModaledit() {
    document.getElementById('modaledit').style.display = 'none';
    document.getElementById('overlay').classList.remove('active');
}

// Your existing calendar functions remain the same
function showCal() {
    const calendar = document.getElementById('calendar');
    if (calendar) {
        calendar.style.display = calendar.style.display === 'none' ? 'block' : 'none';
    }
}

// Your existing datetime event listener
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById('cal');
    input.addEventListener('change', function () {
        const dateTime = new Date(this.value);
        const date = dateTime.toISOString().split('T')[0];
        const time = dateTime.toTimeString().split(' ')[0];
        localStorage.setItem("newdata", date);
        localStorage.setItem("newtime", time);
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form'); // Select the form element
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting
    });

    const editButtons = document.querySelectorAll('.edit'); // Get all buttons with class 'edit'

    editButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default action

            const row = button.closest('tr'); // Get the row of the clicked button
            const cells = row.getElementsByTagName('td');

            // Access the ID of the appointment
            const appointmentId = cells[1].id;
            console.log('Editing appointment with ID:', appointmentId);

            // Implement your logic to populate modal here
        });
    });
});




