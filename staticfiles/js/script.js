// Data State
const jobData = [
    { id: 1, title: "Python Developer", company: "TechNova", category: "it", salary: "₹55k", icon: "bi-code-slash" },
    { id: 2, title: "HR Manager", company: "City Retail", category: "admin", salary: "₹35k", icon: "bi-person-badge" },
    { id: 3, title: "Marketing Lead", company: "Skyline", category: "sales", salary: "₹45k", icon: "bi-megaphone" }
];

// Scroll Reveal Logic
function reveal() {
    let reveals = document.querySelectorAll(".reveal, .reveal-right");
    reveals.forEach(el => {
        let windowHeight = window.innerHeight;
        let elementTop = el.getBoundingClientRect().top;
        if (elementTop < windowHeight - 100) {
            el.classList.add("active");
        }
    });
}
window.addEventListener("scroll", reveal);
window.onload = reveal; // Trigger on first load

// Render Jobs
const jobContainer = document.getElementById('job-container');
function renderJobs(list) {
    jobContainer.innerHTML = '';
    list.forEach(job => {
        jobContainer.insertAdjacentHTML('beforeend', `
            <div class="col-6 col-md-4 reveal active">
                <div class="job-card shadow-sm h-100">
                    <i class="${job.icon} fs-1 text-primary-gradient mb-3 d-block"></i>
                    <h5 class="fw-800">${job.title}</h5>
                    <p class="text-muted small">${job.company}</p>
                    <div class="d-flex justify-content-between mt-4">
                        <span class="fw-bold">${job.salary}</span>
                        <i class="bi bi-arrow-right-short fs-4"></i>
                    </div>
                </div>
            </div>
        `);
    });
}

// Initial Run
renderJobs(jobData);