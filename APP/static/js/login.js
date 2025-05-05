// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById("password");
    const passwordToggle = document.getElementById("showPassword");
    passwordInput.type = passwordToggle.checked ? "text" : "password";
}

// Validate login form
document.getElementById("loginForm").addEventListener("submit", function(event) {
    const username = document.querySelector("input[name='username']").value.trim();
    const password = document.querySelector("input[name='password']").value.trim();

    // Check if username or password is empty
    if (!username || !password) {
        alert("Both username and password are required.");
        event.preventDefault();
        return;
    }

    // Validate username (letters, numbers, and underscores only)
    const usernamePattern = /^[a-zA-Z0-9_]+$/;
    if (!usernamePattern.test(username)) {
        alert("Username can only contain letters, numbers, and underscores.");
        event.preventDefault();
        return;
    }
});

// Attach toggle event for password visibility
document.getElementById("showPassword").addEventListener("change", togglePassword);

