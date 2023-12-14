const $sidebarToggler  = document.querySelector('#sidebar-toggle');
const $toggleIcon  = document.querySelector('#toggle-icon');
const $wrapper = document.querySelector('#wrapper');
const $userDropdown = document.querySelector('#user-dropdown-toggle');

$sidebarToggler.addEventListener('click', (e) => {
    e.preventDefault();
    $wrapper.classList.toggle('toggled');
    localStorage.setItem('sidebarToggled', $wrapper.classList.contains('toggled'));
    const sidebarToggled = localStorage.getItem('sidebarToggled') === 'true';
    if (sidebarToggled) {
        $wrapper.classList.add('toggled');
        $toggleIcon.className = "fa-solid fa-arrow-right fa-xl";
    }
    else {
        $toggleIcon.className = "fa-solid fa-arrow-left fa-xl";
    }
});

// When the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {

   
    if (sidebarToggled) {
        $wrapper.classList.add('toggled');
        $toggleIcon.className = "fa-solid fa-arrow-right fa-xl";
    }
    else {
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