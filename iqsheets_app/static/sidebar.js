const $sidebarToggler = document.querySelector('#sidebar-toggle');
const $toggleIcon = document.querySelector('#toggle-icon');
const $wrapper = document.querySelector('#wrapper');

// Function to toggle sidebar
function toggleSidebar() {
    const isToggled = $wrapper.classList.toggle('toggled');
    $toggleIcon.className = isToggled ? "fa-solid fa-arrow-right fa-xl" : "fa-solid fa-arrow-left fa-xl";
    localStorage.setItem('sidebarToggled', isToggled);
}

$sidebarToggler.addEventListener('click', (e) => {
    e.preventDefault();
    toggleSidebar();
});

// When the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Apply the initial toggle state from localStorage
    if (localStorage.getItem('sidebarToggled') === 'true') {
        $wrapper.classList.add('toggled');
        $toggleIcon.className = "fa-solid fa-arrow-right fa-xl";
    } else {
        $toggleIcon.className = "fa-solid fa-arrow-left fa-xl";
    }

    // Get all nav items
    var navItems = document.querySelectorAll('.sidebar-nav .nav-item');

    // Add click event to each nav item
    navItems.forEach(function(item) {
        item.addEventListener('click', function() {
            // Remove 'active' class from all nav items
            navItems.forEach(function(nav) {
                nav.classList.remove('active');
            });

            // Add 'active' class to the clicked nav item
            this.classList.add('active');
        });
    });
});