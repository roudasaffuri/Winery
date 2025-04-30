// This script toggles the visibility of the password input field
// when the user clicks the eye icon (show/hide password).
// It changes the input type between 'password' and 'text',
// and also switches the eye icon between open and slashed.
document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.querySelector('.togglePassword');
    const passwordInput = document.querySelector('.password');
    const toggleIcon = document.querySelector('.toggleIcon');

    if (toggleBtn && passwordInput && toggleIcon) {
        toggleBtn.addEventListener('click', () => {
            const isPassword = passwordInput.type === 'password'; // true/false
            passwordInput.type = isPassword ? 'text' : 'password';
            toggleIcon.classList.toggle('fa-eye');
            toggleIcon.classList.toggle('fa-eye-slash');
        });
    }
});
