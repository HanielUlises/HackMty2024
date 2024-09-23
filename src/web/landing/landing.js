// Mobile Menu Toggle
document.addEventListener('alpine:init', () => {
    Alpine.data('mobileMenu', () => ({
        openMenu: false,

        toggleMenu() {
            this.openMenu = !this.openMenu;
        },

        closeMenu() {
            this.openMenu = false;
        }
    }));
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});



