// 1. Data Source (No Job Images)
const jobData = [
    { id: 1, title: "Executive Developer", company: "TechNova", category: "it", salary: "₹8 LPA", icon: "bi-laptop" },
    { id: 2, title: "Chief of Staff", company: "City Plaza", category: "admin", salary: "₹40k/m", icon: "bi-building-gear" },
    { id: 3, title: "Marketing Director", company: "Rainbow Hub", category: "sales", salary: "₹6 LPA", icon: "bi-megaphone" },
    { id: 4, title: "Financial Analyst", company: "Malabar Trading", category: "finance", salary: "₹5 LPA", icon: "bi-calculator" },
    { id: 5, title: "Cloud Architect", company: "Global Cloud", category: "it", salary: "₹12 LPA", icon: "bi-cloud" },
    { id: 6, title: "Sales Executive", company: "Creative Media", category: "sales", salary: "₹35k/m", icon: "bi-graph-up" }
];

const jobContainer = document.getElementById('job-container');

// 2. Render Function
function renderJobs(jobs) {
    jobContainer.innerHTML = '';
    
    if (jobs.length === 0) {
        jobContainer.innerHTML = `<div class="col-12 text-center py-5 text-white opacity-50">No opportunities currently available in this sector.</div>`;
        return;
    }

    jobs.forEach((job, index) => {
        const delay = index * 0.1;
        
        const html = `
            <div class="col-12 col-md-6 col-lg-4 reveal" style="animation-delay: ${delay}s">
                <div class="job-card shadow-lg">
                    <div class="job-card-body">
                        
                        <div class="d-flex justify-content-between align-items-start mb-4">
                            <div class="job-icon-badge">
                                <i class="bi ${job.icon}"></i>
                            </div>
                            <span class="small opacity-75 text-uppercase gold-text fw-bold" style="letter-spacing: 1px;">${job.category}</span>
                        </div>
                        
                        <h5 class="fw-bold text-white mb-1">${job.title}</h5>
                        <p class="small text-white opacity-50 mb-4"><i class="bi bi-buildings me-2"></i>${job.company}</p>
                        
                        <div class="mt-auto d-flex justify-content-between align-items-center pt-3 border-top border-secondary border-opacity-25">
                            <span class="fw-bold gold-text fs-5">${job.salary}</span>
                            <a href="#" class="apply-btn-luxury">View Details <i class="bi bi-arrow-right ms-1"></i></a>
                        </div>
                        
                    </div>
                </div>
            </div>
        `;
        jobContainer.insertAdjacentHTML('beforeend', html);
    });
}

// 3. Filter Logic
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        const filter = this.dataset.filter;
        renderJobs(filter === 'all' ? jobData : jobData.filter(j => j.category === filter));
    });
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    renderJobs(jobData);
});