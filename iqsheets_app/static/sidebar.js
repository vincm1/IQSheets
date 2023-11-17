const $button  = document.querySelector('#sidebar-toggle');
const $wrapper = document.querySelector('#wrapper');

$button.addEventListener('click', (e) => {
  e.preventDefault();
  $wrapper.classList.toggle('toggled');
});

// When the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
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