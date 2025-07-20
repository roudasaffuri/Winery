// This script toggles the visibility of the password input field
// when the user clicks the eye icon (show/hide password).
// It changes the input type between 'password' and 'text',
// and also switches the eye icon between open and slashed.
document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.querySelector('.togglePassword');
    const passwordInput = document.querySelector('.password');
    const toggleIcon = document.querySelector('.toggleIcon');

    // Make sure all required elements exist
    if (toggleBtn && passwordInput && toggleIcon) {
        toggleBtn.addEventListener('click', () => {
            const isHidden = passwordInput.type === 'password';

            // Toggle password visibility
            passwordInput.type = isHidden ? 'text' : 'password';

            // Update icon class
            if (isHidden) {
                toggleIcon.classList.remove('fa-eye');
                toggleIcon.classList.add('fa-eye-slash');
            } else {
                toggleIcon.classList.remove('fa-eye-slash');
                toggleIcon.classList.add('fa-eye');
            }
        });
    }
});


function applyAllWineFilters() {
  // Step 1: Get all the checkboxes that are checked under the wine type filter
  //wine-type-filter-all --> the id of the form
  // search the inputs with the name wine_type_all checked
  const checkboxes = document.querySelectorAll('#wine-type-filter-all input[name="wine_type_all"]:checked');

  // Step 2: Get the values (types "red/white/Sparkling/rose  ) of the checked checkboxes
  // Array.from ["red","Sparkling"]
    const selectedTypes = Array.from(checkboxes).map(checkbox => checkbox.value);

  // Step 3: Get all wine items from the collection
  const wineItems = document.querySelectorAll('#all-wines-collection .wine-item');

  // Step 4: Show or hide each wine item based on the selected filters
  wineItems.forEach(function(item) {
    const wineType = item.dataset.wineType; // Get wine type from data attribute

    // If no checkbox is selected OR the wine type is selected → show it
    if (selectedTypes.length === 0 || selectedTypes.includes(wineType)) {
      item.style.display = 'block'; // Show the item
    } else {
      item.style.display = 'none'; // Hide the item
    }
  });
}
