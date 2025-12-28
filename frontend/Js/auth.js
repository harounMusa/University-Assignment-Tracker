const API_URL = "https://university-assignment-tracker-c69h.onrender.com";

// Handle Login
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        try {
            const res = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();
            
            if (res.ok) {
                // Save the token and username to browser storage
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('username', data.username);
                window.location.href = 'index.html';
            } else {
                alert(data.message);
            }
        } catch (err) {
            console.error(err);
        }
    });
}

// Handle Signup
const signupForm = document.getElementById('signup-form');
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('signup-username').value;
        const password = document.getElementById('signup-password').value;

        try {
            const res = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();

            if (res.ok) {
                alert("Account created! Please login.");
                window.location.href = 'login.html';
            } else {
                alert(data.message);
            }
        } catch (err) {
            console.error(err);
        }
    });
}