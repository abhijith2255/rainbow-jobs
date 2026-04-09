// 1. Array of Demo Jobs
const jobData = [
    {
        id: 1,
        title: "Frontend Developer",
        company: "TechNova Solutions",
        location: "Kochi, Kerala",
        category: "it",
        icon: "bi-laptop",
        salary: "₹5,00,000 LPA"
    },
    {
        id: 2,
        title: "Office Administrator",
        company: "City Plaza Group",
        location: "Kozhikode, Kerala",
        category: "admin",
        icon: "bi-building",
        salary: "₹20,000 / month"
    },
    {
        id: 3,
        title: "Sales Coordinator",
        company: "Rainbow Retail Hub",
        location: "Trivandrum, Kerala",
        category: "sales",
        icon: "bi-graph-up-arrow",
        salary: "₹25,000 + Incentives"
    },
    {
        id: 4,
        title: "Junior Accountant",
        company: "Malabar Trading Co.",
        location: "Kozhikode, Kerala",
        category: "finance",
        icon: "bi-calculator",
        salary: "₹22,000 / month"
    },
    {
        id: 5,
        title: "Python Django Engineer",
        company: "Global Cloud Inc.",
        location: "Remote",
        category: "it",
        icon: "bi-code-slash",
        salary: "₹8,00,000 LPA"
    },
    {
        id: 6,
        title: "Marketing Executive",
        company: "Creative Media",
        location: "Kochi, Kerala",
        category: "sales",
        icon: "bi-megaphone",
        salary: "₹30,000 / month"
    }
];

// 2. Function to Render Jobs to the HTML
const jobContainer = document.getElementById('job-container');

function renderJobs(jobsToRender) {
    // Clear current jobs
    jobContainer.innerHTML = '';

    // If no jobs match, show a message
    if (jobsToRender.length === 0) {
        jobContainer.innerHTML = `
            <div class="col-12 text-center py-5">
                <h5 class="text-muted">No jobs found in this category.</h5>
            </div>
        `;
        return;
    }

    // Loop through jobs and create HTML structure
    jobsToRender.forEach((job, index) => {
        // Add a slight animation delay for each card
        const delay = index * 0.1;
        
        const jobHTML = `
            <div class="col-md-6 col-lg-4 fade-in" style="animation-delay: ${delay}s">
                <div class="card job-card">
                    <div class="card-body p-4">
                        <div class="card-icon-wrap">
                            <i class="bi ${job.icon}"></i>
                        </div>
                        <h5 class="fw-bold mb-1">${job.title}</h5>
                        <p class="text-pink fw-semibold mb-3">${job.company}</p>
                        
                        <div class="small text-muted mb-4">
                            <span class="d-block mb-2"><i class="bi bi-geo-alt-fill text-danger me-2"></i>${job.location}</span>
                            <span class="d-block"><i class="bi bi-cash text-success me-2"></i>${job.salary}</span>
                        </div>
                    </div>
                    <div class="card-footer bg-transparent border-top-0 px-4 pb-4">
                        <a href="#" class="btn btn-outline-dark w-100 rounded-pill">Apply Now</a>
                    </div>
                </div>
            </div>
        `;
        // Inject into the container
        jobContainer.insertAdjacentHTML('beforeend', jobHTML);
    });
}

// 3. Initialize the page with all jobs
renderJobs(jobData);

// 4. Filtering Logic
const filterButtons = document.querySelectorAll('.filter-btn');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove 'active' class from all buttons
        filterButtons.forEach(btn => btn.classList.remove('active'));
        
        // Add 'active' class to the clicked button
        button.classList.add('active');

        // Get the filter category
        const filterValue = button.getAttribute('data-filter');

        // Filter the array
        if (filterValue === 'all') {
            renderJobs(jobData);
        } else {
            const filteredJobs = jobData.filter(job => job.category === filterValue);
            renderJobs(filteredJobs);
        }
    });
});