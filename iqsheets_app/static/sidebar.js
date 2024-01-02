const $sidebarToggler = document.querySelector('#sidebar-toggle');
const $toggleIcon = document.querySelector('#toggle-icon');
const $wrapper = document.querySelector('#wrapper');
const $usermenuDropDown = document.querySelector('#usermenu');
const $usermenuSidebarName = document.querySelector('#usernameid');

// When the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    const isSidebarToggled = localStorage.getItem('sidebarToggled') === 'true';

    // Apply the initial toggle state from localStorage
    if (isSidebarToggled) {
        $wrapper.classList.add('toggled');
        $toggleIcon.className = "fa-solid fa-arrow-right";
        $usermenuDropDown.classList.add('toggled');
        $usermenuSidebarName.classList.add('toggled');
        document.querySelectorAll('.username').forEach(el => el.classList.add('hide-username')); // Hide usernames
        document.querySelectorAll('.dropdown-toggle').forEach(el => el.classList.add('hide-dropdown-toggle')); // Hide usernames
    } else {
        $toggleIcon.className = "fa-solid fa-arrow-left";
        $usermenuDropDown.classList.remove('toggled');
        $usermenuSidebarName.classList.remove('toggled');
        document.querySelectorAll('.username').forEach(el => el.classList.remove('hide-username')); // Show usernames
        document.querySelectorAll('.dropdown-toggle').forEach(el => el.classList.remove('hide-dropdown-toggle')); // Hide usernames
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

// Function to toggle sidebar
function toggleSidebar() {
    const isToggled = $wrapper.classList.toggle('toggled');
    $toggleIcon.className = isToggled ? "fa-solid fa-arrow-right" : "fa-solid fa-arrow-left";
    localStorage.setItem('sidebarToggled', isToggled);
    if (isToggled) {
        $usermenuDropDown.classList.add('toggled');
        $usermenuSidebarName.classList.add('toggled');
        document.querySelectorAll('.username').forEach(el => el.classList.add('hide-username'));
        document.querySelectorAll('.dropdown-toggle').forEach(el => el.classList.add('hide-dropdown-toggle'));
    } else {
        $usermenuDropDown.classList.remove('toggled');
        $usermenuSidebarName.classList.remove('toggled');
        document.querySelectorAll('.username').forEach(el => el.classList.remove('hide-username'));
        document.querySelectorAll('.dropdown-toggle').forEach(el => el.classList.remove('hide-dropdown-toggle')); // Show usernames
        // Restore the inner text for dropdown items if necessary
    }
}

$sidebarToggler.addEventListener('click', (e) => {
    e.preventDefault();
    toggleSidebar();
});

