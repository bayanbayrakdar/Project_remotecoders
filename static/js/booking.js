const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const name_patient = document.getElementById("name_patient")
const age_patient = document.getElementById("age_patient")
const booking_button = document.getElementById("booking_button")
let currentmonth = new Date().getMonth();
let currentyear = new Date().getFullYear();
const booking_form = document.getElementById("booking")
const successMessage = document.getElementById("successMessage")
const monthyear = document.getElementById('month-year');
const days = document.getElementById('days');

console.log("month"+currentmonth)

function rendercal() {

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
const SelectDete = (event) => {
    // Check if the clicked element is a day
    if (event.target && event.target.innerText) {
        const selectedDay = event.target.innerText;
        event.target.style.backgroundColor = 'rgb(139, 197, 199)'
        localStorage.setItem("year",currentyear)
        localStorage.setItem("month",monthNames[currentmonth])
        localStorage.setItem("day",selectedDay)
        

    }
};



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
// Add event listener for day clicks
days.addEventListener("click", SelectDete);

const checkInput = (event) => {
    event.preventDefault()
    year_click=localStorage.getItem("year")
    month_click=localStorage.getItem("month")
    day_click=localStorage.getItem("day")
    
    



    const appointment = {
        name_patient: name_patient.value,
        age_patient: age_patient.value,
        "Date":{"day":day_click,"month":month_click,"year":year_click}

    };
    console.log(appointment.Date.month)
    localStorage.setItem("name_patient", appointment.name_patient)
    localStorage.setItem("age_patient", appointment.age_patient)

    

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
