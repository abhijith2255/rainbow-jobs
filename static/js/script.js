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

// 2. Job Data (Matches your screenshot)
const jobData = [
    { id: 1, title: "Executive Developer", company: "TechNova Solutions", location: "Kochi, Kerala", category: "it", salary: "₹8 LPA", icon: "bi-laptop" },
    { id: 2, title: "Chief of Staff", company: "City Plaza Group", location: "Kozhikode, Kerala", category: "admin", salary: "₹40k/m", icon: "bi-building" },
    { id: 3, title: "Marketing Director", company: "Rainbow Hub", location: "Trivandrum, Kerala", category: "sales", salary: "₹6 LPA", icon: "bi-megaphone" },
    { id: 4, title: "Financial Analyst", company: "Malabar Trading", location: "Kozhikode, Kerala", category: "finance", salary: "₹5 LPA", icon: "bi-calculator" },
    { id: 5, title: "Cloud Architect", company: "Global Cloud", location: "Remote", category: "it", salary: "₹12 LPA", icon: "bi-cloud" },
    { id: 6, title: "Sales Executive", company: "Creative Media", location: "Kochi, Kerala", category: "sales", salary: "₹35k/m", icon: "bi-graph-up" }
];

const jobContainer = document.getElementById('job-container');

// 3. Render NEW Solid Job Cards
function renderJobs(jobs) {
    jobContainer.innerHTML = '';
    
    if (jobs.length === 0) {
        jobContainer.innerHTML = `<div class="col-12 text-center py-5 text-white opacity-50">No opportunities found in this category.</div>`;
        return;
    }

    jobs.forEach((job, index) => {
        const delay = index * 0.1; // Staggered animation
        
        const html = `
            <div class="col-12 col-md-6 col-lg-4 animate-fade-up" style="animation-delay: ${delay}s">
                <div class="job-card">
                    
                    <div class="d-flex justify-content-between align-items-start mb-4">
                        <div class="job-icon-box">
                            <i class="bi ${job.icon}"></i>
                        </div>
                        <div class="job-category-tag">
                            <i class="bi bi-briefcase me-2"></i>${job.category}
                        </div>
                    </div>
                    
                    <h5 class="job-title text-white mb-3">${job.title}</h5>
                    <div class="job-details mb-4">
                        <p class="mb-1"><i class="bi bi-buildings me-2"></i>${job.company}</p>
                        <p class="mb-0"><i class="bi bi-geo-alt me-2"></i>${job.location}</p>
                    </div>

                    <div class="job-card-footer">
                        <span class="job-salary text-gold">${job.salary}</span>
                        <a href="#" class="btn-view-details">View Details</a>
                    </div>
                    
                </div>
            </div>
        `;
        jobContainer.insertAdjacentHTML('beforeend', html);
    });
}

// 4. Category Filter Logic
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        const filter = this.dataset.filter;
        renderJobs(filter === 'all' ? jobData : jobData.filter(j => j.category === filter));
    });
});

// 5. Scroll Reveal Animations (For Sections Below Hero)
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
    renderJobs(jobData);
    revealElements();
});