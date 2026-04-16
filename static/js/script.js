document.addEventListener("DOMContentLoaded", () => {
    
    // 1. DYNAMIC NAVBAR
    const navbar = document.getElementById("main-navbar");
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            navbar.classList.remove("nav-transparent");
            navbar.classList.add("nav-scrolled");
        } else {
            navbar.classList.add("nav-transparent");
            navbar.classList.remove("nav-scrolled");
        }
    });

    // 2. PARALLAX EFFECT
    const parallaxBg = document.querySelector('.parallax-bg');
    window.addEventListener('scroll', () => {
        if(parallaxBg) {
            parallaxBg.style.transform = `translateY(${window.pageYOffset * 0.4}px)`;
        }
    });

    // 3. 3D TILT EFFECT
    const tiltCard = document.querySelector('.tilt-effect');
    if(tiltCard) {
        tiltCard.addEventListener('mousemove', (e) => {
            const rect = tiltCard.getBoundingClientRect();
            const rotateX = (((e.clientY - rect.top) - rect.height / 2) / (rect.height / 2)) * -10;
            const rotateY = (((e.clientX - rect.left) - rect.width / 2) / (rect.width / 2)) * 10;
            tiltCard.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });
        tiltCard.addEventListener('mouseleave', () => {
            tiltCard.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
            tiltCard.style.transition = "transform 0.5s ease";
        });
        tiltCard.addEventListener('mouseenter', () => { tiltCard.style.transition = "none"; });
    }

    // 4. CATEGORY FILTERING
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

    // 5. TYPEWRITER EFFECT
    const textElement = document.getElementById("dynamic-text");
    if(textElement) {
        const words = ["Refined.", "Elevated.", "Mastered.", "Discovered."];
        let wordIndex = 0, charIndex = 0, isDeleting = false;
        function typeEffect() {
            const currentWord = words[wordIndex];
            if (isDeleting) { textElement.textContent = currentWord.substring(0, charIndex - 1); charIndex--; } 
            else { textElement.textContent = currentWord.substring(0, charIndex + 1); charIndex++; }
            
            let typingSpeed = isDeleting ? 50 : 120;
            if (!isDeleting && charIndex === currentWord.length) { typingSpeed = 2000; isDeleting = true; } 
            else if (isDeleting && charIndex === 0) { isDeleting = false; wordIndex = (wordIndex + 1) % words.length; typingSpeed = 500; }
            setTimeout(typeEffect, typingSpeed);
        }
        setTimeout(typeEffect, 1000);
    }

    // 6. SCROLL REVEAL
    const revealElements = document.querySelectorAll(".reveal");
    const revealOnScroll = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("active");
            observer.unobserve(entry.target);
        });
    }, { threshold: 0.15, rootMargin: "0px 0px -50px 0px" });
    revealElements.forEach(el => revealOnScroll.observe(el));

    // 7. GOLD PARTICLE NETWORK
    const canvas = document.getElementById('particle-canvas');
    if(canvas) {
        const ctx = canvas.getContext('2d');
        let particlesArray;
        canvas.width = window.innerWidth; canvas.height = document.getElementById('hero').offsetHeight;

        class Particle {
            constructor(x, y, directionX, directionY, size, color) {
                this.x = x; this.y = y; this.directionX = directionX; this.directionY = directionY;
                this.size = size; this.color = color;
            }
            draw() { ctx.beginPath(); ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false); ctx.fillStyle = this.color; ctx.fill(); }
            update() {
                if (this.x > canvas.width || this.x < 0) { this.directionX = -this.directionX; }
                if (this.y > canvas.height || this.y < 0) { this.directionY = -this.directionY; }
                this.x += this.directionX; this.y += this.directionY; this.draw();
            }
        }
        function init() {
            particlesArray = [];
            let numberOfParticles = (canvas.height * canvas.width) / 12000; 
            for (let i = 0; i < numberOfParticles; i++) {
                let size = (Math.random() * 2) + 1;
                let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
                let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
                let directionX = (Math.random() * 1.5) - 0.75;
                let directionY = (Math.random() * 1.5) - 0.75;
                let color = 'rgba(212, 175, 55, 0.8)'; // Pure Gold
                particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
            }
        }
        function connect() {
            for (let a = 0; a < particlesArray.length; a++) {
                for (let b = a; b < particlesArray.length; b++) {
                    let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x)) + ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
                    if (distance < (canvas.width / 7) * (canvas.height / 7)) {
                        ctx.strokeStyle = 'rgba(212, 175, 55,' + (0.2 - (distance / 40000)) + ')';
                        ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(particlesArray[a].x, particlesArray[a].y); ctx.lineTo(particlesArray[b].x, particlesArray[b].y); ctx.stroke();
                    }
                }
            }
        }
        function animate() { requestAnimationFrame(animate); ctx.clearRect(0, 0, canvas.width, canvas.height); for (let i = 0; i < particlesArray.length; i++) { particlesArray[i].update(); } connect(); }
        window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = document.getElementById('hero').offsetHeight; init(); });
        init(); animate();
    }
});