const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const name_patient = document.getElementById("name_patient")
const age_patient = document.getElementById("age_patient")
const booking_button = document.getElementById("booking_button")
let currentmonth = new Date().getMonth();
let currentyear = new Date().getFullYear();
const booking_form = document.getElementById("booking")
const successMessage = document.getElementById("successMessage")



function rendercal() {
    const monthyear = document.getElementById('month-year');
    const days = document.getElementById('days');
    days.innerHTML = '';
    const firstday = new Date(currentyear, currentmonth, 1).getDay();
    const totaldays = new Date(currentyear, currentmonth + 1, 0).getDate();
    monthyear.innerText = `${monthNames[currentmonth]} ${currentyear}`;
    for (let i = 0; i < firstday; i++) {
        days.innerHTML += '<div></div>';
    }
    for (let day = 1; day <= totaldays; day++) {
        days.innerHTML += `<div>${day}</div>`;
    }
}

function changemonth(dir) {
    currentmonth += dir;
    if (currentmonth < 0) {
        currentmonth = 11;
        currentyear--;
    } else if (currentmonth > 11) {
        currentmonth = 0;
        currentyear++;
    }
    rendercal();
}

rendercal();

const checkInput = (event) => {
    event.preventDefault()
    const appointment = {
        name_patient: name_patient.value,
        age_patient: age_patient.value,

    };
    localStorage.setItem("name_patient", appointment.name_patient)
    localStorage.setItem("age_patient", appointment.age_patient)

    console.log("ss")

    // Example using fetch
    fetch('/booking', {
        method: 'POST', // Make sure this matches the allowed methods in your Flask route
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(appointment),
    }).then(response => {
        return response.json();
    }).then(data => {
        successMessage.style.display = "block";
        successMessage.innerHTML = data.message;
    }).catch(error => {
        console.error('Error:', error);
        
    })
}

booking_form.addEventListener("submit", checkInput)
