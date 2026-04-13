// 1. Transparent Navbar Scroll Effect
const navbar = document.getElementById('main-navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('nav-scrolled');
        navbar.classList.remove('nav-transparent');
    } else {
        navbar.classList.add('nav-transparent');
        navbar.classList.remove('nav-scrolled');
    }
});

// 2. Category Filter Logic (Filters the REAL Database Jobs from Django)
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        // Remove active class from all buttons, add to the clicked one
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        const filterValue = this.dataset.filter;
        const jobItems = document.querySelectorAll('.job-item');

        // Loop through the actual HTML cards Django created
        jobItems.forEach(item => {
            if (filterValue === 'all' || item.classList.contains(filterValue)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
});

// 3. Scroll Reveal Animations (For Sections Below Hero)
function revealElements() {
    const reveals = document.querySelectorAll(".reveal");
    reveals.forEach(el => {
        const windowHeight = window.innerHeight;
        const elementTop = el.getBoundingClientRect().top;
        if (elementTop < windowHeight - 50) {
            el.classList.add("active");
        }
    });
}
window.addEventListener("scroll", revealElements);

// Initialize on Load
document.addEventListener('DOMContentLoaded', () => {
    revealElements();
});