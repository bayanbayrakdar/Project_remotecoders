const username_login = document.getElementById("username_login");
const password_login = document.getElementById("password_login");
const loginForm = document.getElementById("loginForm");
const button_login = document.getElementById("button_login");

const username = username_login.value;
const password = password_login.value;

// Store values in localStorage (if you want to)
localStorage.setItem("username", username);
localStorage.setItem("password", password);

console.log("kkk");

function login(event) {
    event.preventDefault(); // Prevent default form submission

    // Get values from the form
    const username = username_login.value;
    const password = password_login.value;

    // Store values in localStorage (if you want to)
    localStorage.setItem("username", username);
    localStorage.setItem("password", password);

    // Create login data object
    const loginData = {
        username: username,
        password: password,
    };


    fetch('/home', {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message); // Show success or error message
        if (data.success) {
            // Redirect or perform further actions on successful login
            window.location.href = "/home"; // This will redirect to home page if needed
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });


}

// Attach event listener to the form
if (loginForm) {
    loginForm.addEventListener("submit", login);
} else {
    console.error("Login form not found!");
}
