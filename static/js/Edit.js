

const name_patient = document.getElementById("name_patient")
const age_patient = document.getElementById("age_patient")
const newbooking_button=document.getElementById("newbooking_button")
//delet item 


document.addEventListener('DOMContentLoaded', () => {
    

    const delete_reservation = (event) => {

        event.preventDefault();
        localStorage.removeItem("name_patient");
        localStorage.removeItem("age_patient");
        localStorage.removeItem("day");
        localStorage.removeItem("year");
        localStorage.removeItem("month");
        localStorage.removeItem("Hour");
        localStorage.removeItem("minute")
        
        
        
        
    };

    if (delete_button) {
        delete_button.addEventListener("click", delete_reservation);
    }
    else{
        console.error("erro");
        
    }

})
function removeRow(button) {
    // Get the row containing the button
    const row = button.parentElement.parentElement;
    // Remove the row from the table
    row.remove();
}

document.addEventListener("DOMContentLoaded", function() {
    function addRow(event) {
        // event.preventDefault();
    
        const table = document.getElementById('outputTable').getElementsByTagName('tbody')[0];
    
        const newdata = localStorage.getItem("newdata");
        const newtime = localStorage.getItem("newtime");

        const newRow = table.insertRow(); 
    
        const cell1 = newRow.insertCell(0);
        const cell2 = newRow.insertCell(1);
        const cell3 = newRow.insertCell(2);
        const cell4 = newRow.insertCell(3);
        const cell5 = newRow.insertCell(4);
        const cell6 = newRow.insertCell(5);
    
        cell1.innerHTML = "0"; // Replace with a dynamic ID if necessary
        cell2.innerHTML = name_patient.value; 
        cell3.innerHTML = age_patient.value; 
        cell4.innerHTML = newdata || "No Data"; 
        cell5.innerHTML = newtime || "No Time"; 
        cell6.innerHTML = `
            <button class="save">Save</button>
            <button class="btn btn-success" data-toggle="modal" data-target="#myModal">Edit</button>
            <button class="delete" onclick="removeRow(this)">Delete</button>
        `;


        // const newAppointment={
        //     "name_patient":  name_patient.value,
        //     "age_patient": age_patient.value,
        //     "Date": {
        //       "day": newdata.day,
        //       "month": newdata.month,
        //       "year": newdata.year
        //     },
        //     "Time": {
        //       "Hour": newtime.Hour,
        //       "Minute": newtime.Minute
        //     }

        // }




        // fetch('/veiw_booking', {  // Adjust the endpoint as needed
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify(newAppointment),
        // })
        // .then(response => {
        //     if (!response.ok) {
        //         throw new Error('Network response was not ok');
        //     }
        //     return response.json();
        // })
        // .then(data => {
        //     alert(data.message); // Show success or error message

        // })
        // .catch(error => {
        //     console.error('Error:', error);
        // });
    


    }

    const newbooking_button = document.getElementById('newbooking_button'); // Make sure to select the correct button
    if (newbooking_button) {
        newbooking_button.addEventListener('click', addRow); // Use 'click' instead of 'submit'
    }
});




function showModal() {
    document.getElementById('modal').style.display = 'block';
    document.getElementById('overlay').classList.add('active');
}

function hideModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('overlay').classList.remove('active');
}


function showCal() {
    const calendar = document.getElementById('calendar');
    if (calendar) {
        // Toggle calendar display
        calendar.style.display = calendar.style.display === 'none' ? 'block' : 'none';
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const input = document.getElementById('cal');
    input.addEventListener('change', function() {
        const dateTime = new Date(this.value);
        const date = dateTime.toISOString().split('T')[0]; // YYYY-MM-DD
        const time = dateTime.toTimeString().split(' ')[0]; // HH:MM:SS
        localStorage.setItem("newdata",date)
        localStorage.setItem("newtime",time)


    });
});


// const newappointment={
//     name_patient: name_patient.value,
//     age_patient: age_patient.value,
//     newdata:newdata,
//     newtime:newtime
// }
// console.log(newappointment)