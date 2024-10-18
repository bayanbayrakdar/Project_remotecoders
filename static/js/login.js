document.addEventListener("DOMContentLoaded", function() {
    const username_login = document.getElementById("username_login");
    const password_login = document.getElementById("password_login");
    const loginForm = document.getElementById("loginForm");

    function login(event) {
        event.preventDefault(); // Prevent default form submission

        const loginData = {
            username: username_login.value,
            password: password_login.value,
        };

        // Send data to Flask server for verification
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Show success or error message
            if (data.success) {
                // Redirect or perform further actions on successful login
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Attach event listener to form
    if (loginForm) {
        loginForm.addEventListener("submit", login);
    } else {
        console.error("Login form not found!");
    }
});


// var button = document.getElementById("button1");
// button.setAttribute("onclick", "move();");
// function move() {
//     window.location.href = "file:///C:/Users/User/source/repos/Trivia/Main.html";
// }