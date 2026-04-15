document.addEventListener("DOMContentLoaded", () => {
    
    // ==========================================
    // 1. DYNAMIC NAVBAR ON SCROLL
    // ==========================================
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

    // ==========================================
    // 2. PARALLAX BACKGROUND EFFECT
    // ==========================================
    const parallaxBg = document.querySelector('.parallax-bg');
    window.addEventListener('scroll', () => {
        let scrolled = window.pageYOffset;
        if(parallaxBg) {
            // Moves the background slower than the scroll speed
            parallaxBg.style.transform = `translateY(${scrolled * 0.4}px)`;
        }
    });

    // ==========================================
    // 3. 3D TILT EFFECT FOR CEO CARD
    // ==========================================
    const tiltCard = document.querySelector('.tilt-effect');
    if(tiltCard) {
        tiltCard.addEventListener('mousemove', (e) => {
            const rect = tiltCard.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -10; // Max 10 degree tilt
            const rotateY = ((x - centerX) / centerX) * 10;
            
            tiltCard.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });
        
        tiltCard.addEventListener('mouseleave', () => {
            tiltCard.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
            tiltCard.style.transition = "transform 0.5s ease";
        });
        
        tiltCard.addEventListener('mouseenter', () => {
            tiltCard.style.transition = "none";
        });
    }

    // ==========================================
    // 4. CATEGORY FILTERING (BOOTSTRAP GRID SAFE)
    // ==========================================
    const filterBtns = document.querySelectorAll(".filter-btn");
    const jobItems = document.querySelectorAll(".job-item");

    filterBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            // Remove active state from all buttons
            filterBtns.forEach(b => b.classList.remove("active"));
            // Add active state to the clicked button
            btn.classList.add("active");

            const filterValue = btn.getAttribute("data-filter");

            jobItems.forEach(item => {
                if (filterValue === "all" || item.classList.contains(filterValue)) {
                    // Show the item safely without breaking the Bootstrap Grid
                    item.classList.remove("d-none");
                    // Small delay to allow display to register before fading in
                    setTimeout(() => {
                        item.style.opacity = "1";
                        item.style.transform = "scale(1)";
                    }, 50);
                } else {
                    // Hide the item smoothly
                    item.style.opacity = "0";
                    item.style.transform = "scale(0.9)";
                    // Wait for CSS transition to finish before removing from document flow
                    setTimeout(() => {
                        item.classList.add("d-none");
                    }, 300); 
                }
            });
        });
    });

    // ==========================================
    // 5. TYPEWRITER / ROTATING TEXT EFFECT
    // ==========================================
    const textElement = document.getElementById("dynamic-text");
    if(textElement) {
        const words = ["Refined.", "Elevated.", "Mastered.", "Discovered."];
        let wordIndex = 0; 
        let charIndex = 0; 
        let isDeleting = false;

        function typeEffect() {
            const currentWord = words[wordIndex];
            
            if (isDeleting) {
                textElement.textContent = currentWord.substring(0, charIndex - 1); 
                charIndex--;
            } else {
                textElement.textContent = currentWord.substring(0, charIndex + 1); 
                charIndex++;
            }
            
            let typingSpeed = isDeleting ? 50 : 120;
            
            if (!isDeleting && charIndex === currentWord.length) {
                typingSpeed = 2000; // Pause when word is fully typed
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false; 
                wordIndex = (wordIndex + 1) % words.length; // Move to next word
                typingSpeed = 500; // Pause before typing next word
            }
            setTimeout(typeEffect, typingSpeed);
        }
        setTimeout(typeEffect, 1000);
    }

    // ==========================================
    // 6. SCROLL REVEAL ANIMATIONS
    // ==========================================
    const revealElements = document.querySelectorAll(".reveal");
    const revealOnScroll = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("active");
            observer.unobserve(entry.target); // Stop observing once revealed
        });
    }, { 
        threshold: 0.15, 
        rootMargin: "0px 0px -50px 0px" 
    });
    
    revealElements.forEach(el => revealOnScroll.observe(el));

    // ==========================================
    // 7. EXECUTIVE PARTICLE NETWORK ENGINE
    // ==========================================
    const canvas = document.getElementById('particle-canvas');
    if(canvas) {
        const ctx = canvas.getContext('2d');
        let particlesArray;

        // Set canvas to full screen of the hero section
        canvas.width = window.innerWidth;
        canvas.height = document.getElementById('hero').offsetHeight;

        class Particle {
            constructor(x, y, directionX, directionY, size, color) {
                this.x = x; 
                this.y = y; 
                this.directionX = directionX; 
                this.directionY = directionY;
                this.size = size; 
                this.color = color;
            }
            // Draw particle
            draw() {
                ctx.beginPath(); 
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
                ctx.fillStyle = this.color; 
                ctx.fill();
            }
            // Move particle and bounce off edges
            update() {
                if (this.x > canvas.width || this.x < 0) { this.directionX = -this.directionX; }
                if (this.y > canvas.height || this.y < 0) { this.directionY = -this.directionY; }
                this.x += this.directionX; 
                this.y += this.directionY;
                this.draw();
            }
        }

        function init() {
            particlesArray = [];
            // Calculate number of particles based on screen size (Density)
            let numberOfParticles = (canvas.height * canvas.width) / 15000; 
            
            for (let i = 0; i < numberOfParticles; i++) {
                let size = (Math.random() * 2) + 1;
                let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
                let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
                let directionX = (Math.random() * 1) - 0.5;
                let directionY = (Math.random() * 1) - 0.5;
                let color = 'rgba(212, 175, 55, 0.8)'; // Gold color matches CSS --gold-accent
                
                particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
            }
        }

        // Check distance between particles to draw connecting lines
        function connect() {
            let opacityValue = 1;
            for (let a = 0; a < particlesArray.length; a++) {
                for (let b = a; b < particlesArray.length; b++) {
                    let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x)) + 
                                   ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
                                   
                    if (distance < (canvas.width / 7) * (canvas.height / 7)) {
                        opacityValue = 1 - (distance / 20000);
                        ctx.strokeStyle = 'rgba(212, 175, 55,' + opacityValue + ')';
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                        ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                        ctx.stroke();
                    }
                }
            }
        }

        // Animation Loop
        function animate() {
            requestAnimationFrame(animate);
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particlesArray.length; i++) { 
                particlesArray[i].update(); 
            }
            connect();
        }

        // Handle window resize
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = document.getElementById('hero').offsetHeight;
            init();
        });

        init();
        animate();
    }
});