const button_login=document.getElementById("button_login")
const button_logout=document.getElementById("logout")
const buttton_clear=document.getElementById("clear")
const doctor_name=document.getElementById("doctor_id")
const doctor_id=document.getElementById("doctor_name")

localStorage.setItem("doctor_name",doctor_name)
localStorage.setItem("doctor_id",doctor_id)
function removeUser(){

    localStorage.removeItem("username")
    localStorage.removeItem("password")

}

function clearAllData() {
    localStorage.clear(); // This clears all data from localStorage
}

// // Example: Add an event listener to a button to clear localStorage
// document.getElementById("clearButton").addEventListener("click", clearAllData);

// button_logout.addEventListener("click",removeUser)

