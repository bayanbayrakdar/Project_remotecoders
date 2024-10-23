const button_login=document.getElementById("button_login")
const button_logout=document.getElementById("logout")
const buttton_clear=document.getElementById("clear")
// button_login.addEventListener("click", ()=>{window.location.href="/login"})
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

