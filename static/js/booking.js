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
let currentHour = new Date().getHours();
let currentMin=new Date().getMinutes()
const timeDisplay = document.getElementById('timeDisplay');
const minutesDisplay=document.getElementById("minDisplay")

function displayTime() {
    timeDisplay.innerHTML = `Current Hour: ${currentHour}`;
    
}
function displayMin() {
    minutesDisplay.innerHTML=`Current minutes: ${currentMin}`;
}

function changeTime(count) {
    currentHour += count; // Adjust the hour based on count
    
    if (currentHour < 0 ) {
        currentHour = 23; // Wrap around to 23 if going below 0
        
    } else if (currentHour >= 24 ) {
        currentHour = 0; // Wrap around to 0 if exceeding 23
        
    }
    displayTime(); // Update the display
    localStorage.setItem("Hour",currentHour)
}
function changeMin(count) {
    // Adjust the min based on count
    currentMin+=count
    if (currentMin<0) {
        
        currentMin =60
    } else if ( currentMin>60) {
        
        currentMin = 0
    }
    displayMin(); // Update the display
    localStorage.setItem("minute",currentMin)
}

// Initial display
displayTime();

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
    Hour=localStorage.getItem("Hour")
    minute=localStorage.getItem("minute")
    
    
    



    const appointment = {
        name_patient: name_patient.value,
        age_patient: age_patient.value,
        "Date":{"day":day_click,"month":month_click,"year":year_click},
        "Time":{"Hour" : Hour , "Minute" : minute}

    };
    
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
//submit booking
booking_form.addEventListener("submit", checkInput)

//Edit booking 




