document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('booking');
    const modal = document.getElementById('modal');

    // Handle Add Button click
    document.addEventListener('click', (event) => {
        if (event.target.getAttribute('id') === 'AddButton') {
            event.preventDefault();
            showModal();
        }
    });

    // Handle form submission
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent form from submitting traditionally

        const IdPatient = form.getAttribute('data-id');

        // Get form values
        const namePatient = document.getElementById('newname_patient').value;
        const agePatient = document.getElementById('newage_patient').value;
        const dateTimeInput = document.getElementById('cal').value;

        // Split datetime into date and time
        const dateTime = new Date(dateTimeInput);
        const newdata = dateTime.toLocaleDateString();
        const newtime = dateTime.toLocaleTimeString();

        // Save to localStorage if needed
        localStorage.setItem("newdata", newdata);
        localStorage.setItem("newtime", newtime);

        addRow(IdPatient);
        hideModal();
    });
});


function addRow(IdPatient) {
    const table = document.getElementById('outputTable').getElementsByTagName('tbody')[0];

    const newdata = localStorage.getItem("newdata");
    const newtime = localStorage.getItem("newtime");
    const namePatient = document.getElementById('newname_patient').value;
    const agePatient = document.getElementById('newage_patient').value;
    const specializationSelect = document.getElementById('specialization-select');
    const selectedSpecialization = specializationSelect.value;

    const newRow = table.insertRow();
    
    // Define single cell content
    const cellContent = IdPatient; // Just inserting the IdPatient
    
    // Insert single cell
    const cell = newRow.insertCell(0);
    cell.innerHTML = cellContent;

    const appointmentData = {
        namePatient: namePatient,
        agePatient: agePatient,
        selectedSpecialization: selectedSpecialization,
        appointmentDate: newdata,
        appointmentTime: newtime
    };

    // Send to server
    fetch('/veiw_booking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(appointmentData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}




const formtable = document.getElementById('booking');
if (formtable) {
    const IdPatient = formtable.getAttribute("data-id");
    formtable.addEventListener('submit', () => {
        // event.preventDefault();

        addRow(IdPatient)
    });

} else {
    console.error('Booking form not found');
}

function GetCal(event) {
    event.preventDefault()
    const cal = document.getElementById("caledit")
    console.log(cal.value)


}


//this is for backend to edit 
document.addEventListener('click', (e) => {


    if (e.target.getAttribute('id') === 'buttonEDit') {
        showModaledit();
        const appointmentId = e.target.getAttribute("data-id");
        const IdPatient = document.getElementById("IdPatient").innerText

        localStorage.setItem("appointmentId", appointmentId);
        localStorage.setItem("IdPatient", IdPatient);
    }


    if (e.target.getAttribute('id') === 'confermEdit') {
        e.preventDefault()
        const dateTimeInput = document.getElementById("caledit").value; // Get the date and time input
        console.log(dateTimeInput);


        const appointmentId = localStorage.getItem("appointmentId");
        const IdPatient = localStorage.getItem("IdPatient");


        const [dateStr, timeStr] = dateTimeInput.split('T');


        updateTable(IdPatient, appointmentId, dateStr, timeStr);


        hideModaledit();
    }
});

// Function to update the table
function updateTable(IdPatient, appointmentId, date, time) {
    // Find the table row corresponding to the appointmentId
    const row = document.querySelector(`tr[data-id="${appointmentId}"]`);
    if (row) {

        row.querySelector('.date-column').textContent = date;
        row.querySelector('.time-column').textContent = time;
    } else {
        console.error('No row found for appointment ID:', appointmentId);
    }
    const updateDate = {
        IdPatient: IdPatient,
        appointmentId: appointmentId,
        date: date,
        time: time,
    }
    fetch('/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateDate)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            if (data.success) {
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}




document.addEventListener('click', (e) => {
    e.stopPropagation();

    if (e.target.getAttribute('id') === 'buttonDELET') {
        e.preventDefault();

        const appointmentId = e.target.getAttribute("appointment_id");
        const row = e.target.closest('tr');
        const IdPatient = row.cells[0].innerText;


        localStorage.setItem("appointmentIddelete", appointmentId);
        localStorage.setItem("IdPatientdelete", IdPatient);


        const storedAppointmentId = localStorage.getItem("appointmentIddelete");
        const storedIdPatient = localStorage.getItem("IdPatientdelete");
        removeRow(storedIdPatient, storedAppointmentId);

        // Remove the row from the UI
        removerow(e.target);
    }
});

// Keep this as a separate function for UI removal
function removerow(button) {
    const row = button.closest('tr');
    if (row) {
        row.remove();
    }
}


function removeRow(IdPatient, appointmentId) {
    const removedata = {
        IdPatient: IdPatient,
        appointmentId: appointmentId,
    };

    fetch('/delete', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(removedata)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting appointment');
        });
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
    // Get input elements
    const input = document.getElementById('cal');

    input.addEventListener('change', function () {
        const dateTime = new Date(this.value);
        const date = dateTime.toISOString().split('T')[0];
        const time = dateTime.toTimeString().split(' ')[0];
        localStorage.setItem("newdata", date);
        localStorage.setItem("newtime", time);

    });
});








