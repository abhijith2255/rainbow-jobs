document.addEventListener("DOMContentLoaded", () => {
    
    // 1. CATEGORY FILTERING (GRID SAFE)
    const filterBtns = document.querySelectorAll(".filter-btn");
    const jobItems = document.querySelectorAll(".job-item");
    const emptyMessage = document.getElementById("empty-job-message");

    filterBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            filterBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            const filterValue = btn.getAttribute("data-filter");
            let visibleCount = 0; 

            jobItems.forEach(item => {
                if (filterValue === "all" || item.classList.contains(filterValue)) {
                    item.classList.remove("d-none");
                    visibleCount++;
                    setTimeout(() => { item.style.opacity = "1"; item.style.transform = "scale(1)"; }, 50);
                } else {
                    item.style.opacity = "0"; item.style.transform = "scale(0.9)";
                    setTimeout(() => { item.classList.add("d-none"); }, 300); 
                }
            });

            if (emptyMessage) {
                if (visibleCount === 0) { setTimeout(() => { emptyMessage.classList.remove("d-none"); }, 300); } 
                else { emptyMessage.classList.add("d-none"); }
            }
        });
    });

    // 2. SCROLL REVEAL & NUMBER COUNTER
    const revealElements = document.querySelectorAll(".reveal");
    const counters = document.querySelectorAll(".counter");
    
    const revealOnScroll = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("active");
            
            // If the revealed element contains number counters, animate them
            if(entry.target.querySelector('.counter')) {
                counters.forEach(counter => {
                    const updateCount = () => {
                        const target = +counter.getAttribute('data-target');
                        const count = +counter.innerText;
                        const inc = target / 40; 
                        if (count < target) {
                            counter.innerText = Math.ceil(count + inc);
                            setTimeout(updateCount, 40);
                        } else {
                            counter.innerText = target;
                        }
                    };
                    updateCount();
                });
            }
            observer.unobserve(entry.target);
        });
    }, { threshold: 0.15, rootMargin: "0px 0px -50px 0px" });
    
    revealElements.forEach(el => revealOnScroll.observe(el));
});