const username = document.getElementById("name");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirm = document.getElementById("confirm");
const button_signup = document.getElementById("button_signup");

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("signupForm"); 

    if (form) {
        form.addEventListener("submit", signup);
    }

    function signup(event) {
        event.preventDefault();

        // Here, we are not initializing id_patient in the frontend, it's managed by the backend
        const userData = {
            username: username.value,
            email: email.value,
            password: password.value,
            confirm: confirm.value,
        };

        // Store in localStorage
        localStorage.setItem("username_signup", userData.username);
        localStorage.setItem("email_signup", userData.email);
        localStorage.setItem("password_signup", userData.password);
        localStorage.setItem("confirm_password", userData.confirm);
        
        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message); });
            }
            return response.json();  // Parse JSON from the response
        })
        .then(data => {
            console.log(data.message);  // Handle the success message
            // Redirect to the home page on successful registration
            window.location.href = '/home';  // Change this to your home URL
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            // Optionally display an error message to the user
        });
    }
});
