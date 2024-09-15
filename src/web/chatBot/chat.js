document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const miniSidebar = document.querySelector('.mini-sidebar');

    // Listen for the end of the transition on the sidebar
    sidebar.addEventListener('transitionend', () => {
        editor.layout(); 
    });

    miniSidebar.addEventListener('transitionend', () => {
        editor.layout(); 
    });
});
