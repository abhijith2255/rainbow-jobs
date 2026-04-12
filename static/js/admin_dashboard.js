document.addEventListener("DOMContentLoaded", function() {
    
    const sidebarToggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    // Handle Mobile Sidebar Toggle
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
    }

    // Close sidebar if clicking outside on mobile
    document.addEventListener('click', function(event) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggleButton = sidebarToggleBtn.contains(event.target);
        
        if (!isClickInsideSidebar && !isClickOnToggleButton && window.innerWidth <= 768) {
            sidebar.classList.remove('open');
        }
    });

    // Add subtle hover animations to stat cards
    const cards = document.querySelectorAll('.stat-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-3px)';
            card.style.transition = 'transform 0.3s ease';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
});