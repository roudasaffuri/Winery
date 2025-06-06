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



function applyAllWineFilters() {
const checkedTypes = Array.from(document.querySelectorAll('#wine-type-filter-all input[name="wine_type_all"]:checked'))
  .map(checkbox => checkbox.value);
const allWineItems = document.querySelectorAll('#all-wines-collection .wine-item.all-wine');

allWineItems.forEach(item => {
  const wineType = item.dataset.wineType;
  if (checkedTypes.length === 0 || checkedTypes.includes(wineType)) {
    item.style.display = 'block';
  } else {
    item.style.display = 'none';
  }
});
}

