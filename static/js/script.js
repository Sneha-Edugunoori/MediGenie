        // Mobile Menu Animation
        const mobileMenu = document.getElementById('mobile-menu');
        const navMenu = document.getElementById('nav-menu');
        const navbar = document.getElementById('navbar');

        if (mobileMenu && navMenu) {
            mobileMenu.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                mobileMenu.classList.toggle('active');
            });

            // Close mobile menu when clicking nav items
            document.querySelectorAll('.nav-item a').forEach(item => {
                item.addEventListener('click', () => {
                    navMenu.classList.remove('active');
                    mobileMenu.classList.remove('active');
                });
            });
        }

        // Particle System
        function createParticleSystem() {
            const particlesContainer = document.getElementById('particles');
            if (!particlesContainer) return;
            
            const particleCount = window.innerWidth < 768 ? 20 : 40;

            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                const size = Math.random() * 4 + 2;
                const startX = Math.random() * window.innerWidth;
                const animationDuration = Math.random() * 25 + 20;
                const animationDelay = Math.random() * 25;
                particle.style.cssText = `
                    width: ${size}px;
                    height: ${size}px;
                    left: ${startX}px;
                    animation-duration: ${animationDuration}s;
                    animation-delay: -${animationDelay}s;
                `;
                particlesContainer.appendChild(particle);
            }
        }

        // Medical Icons Generation
        function createMedicalIcons() {
            const iconsContainer = document.getElementById('medical-icons');
            if (!iconsContainer) return;
            
            const icons = ['fa-plus', 'fa-heart', 'fa-stethoscope', 'fa-user-md', 'fa-pills', 'fa-dna', 'fa-microscope', 'fa-thermometer'];
            const iconCount = window.innerWidth < 768 ? 6 : 12;

            for (let i = 0; i < iconCount; i++) {
                const icon = document.createElement('i');
                const randomIcon = icons[Math.floor(Math.random() * icons.length)];
                icon.className = `fas ${randomIcon} medical-icon-animated`;
                const x = Math.random() * 100;
                const y = Math.random() * 100;
                const size = Math.random() * 1.5 + 1;
                const animationDelay = Math.random() * 15;
                const animationDuration = Math.random() * 10 + 12;
                icon.style.cssText = `
                    left: ${x}%;
                    top: ${y}%;
                    font-size: ${size}rem;
                    animation-delay: ${animationDelay}s;
                    animation-duration: ${animationDuration}s;
                `;
                iconsContainer.appendChild(icon);
            }
        }

        // Smooth Scrolling
        function smoothScroll(target, duration = 800) {
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - 100;
            const startPosition = window.pageYOffset;
            const distance = targetPosition - startPosition;
            let startTime = null;

            function animation(currentTime) {
                if (startTime === null) startTime = currentTime;
                const timeElapsed = currentTime - startTime;
                const progress = Math.min(timeElapsed / duration, 1);
                const ease = progress < 0.5 ? 2 * progress * progress : 1 - Math.pow(-2 * progress + 2, 2) / 2;
                window.scrollTo(0, startPosition + distance * ease);
                if (timeElapsed < duration) requestAnimationFrame(animation);
            }
            requestAnimationFrame(animation);
        }

        // Navigation Scroll Effects
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) smoothScroll(target);
            });
        });

        // Intersection Observer for Feature Cards
        function createObserver() {
            const observerOptions = {
                threshold: 0.2,
                rootMargin: '0px 0px -50px 0px'
            };
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const delay = entry.target.dataset.animationDelay || 0;
                        setTimeout(() => entry.target.classList.add('animate'), delay);
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);
            document.querySelectorAll('.feature-card').forEach(card => observer.observe(card));
        }

        // Navbar Scroll Effects
        function handleNavbarScroll() {
            let ticking = false;
            function updateNavbar() {
                const scrolled = window.pageYOffset;
                if (navbar) {
                    if (scrolled > 80) navbar.classList.add('scrolled');
                    else navbar.classList.remove('scrolled');
                }
                ticking = false;
            }
            window.addEventListener('scroll', () => {
                if (!ticking) {
                    requestAnimationFrame(updateNavbar);
                    ticking = true;
                }
            });
        }

        // Fixed Modal Functions
        const modal = document.getElementById('getStartedModal');
        const getStartBtn = document.getElementById('getStartBtn');
        const closeBtn = document.querySelector('.close');

        function openModal() {
            if (modal) {
                modal.classList.add('show');
                document.body.style.overflow = 'hidden'; // Prevent background scrolling
            }
        }

        function closeModal() {
            if (modal) {
                modal.classList.remove('show');
                document.body.style.overflow = ''; // Restore scrolling
            }
        }

        // portal selction
        // const portalUrls = {
        //     patient: "{{ url_for('patient_signup') }}",
        //     doctor: "{{ url_for('doctor_signup') }}",
        //     government: "{{ url_for('gov_signup') }}"
        // };

        function selectPortal(portalType) {
            closeModal();
            window.location.href = portalUrls[portalType];
        }

        // Event Listeners
        if (getStartBtn) {
            getStartBtn.addEventListener('click', openModal);
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', closeModal);
        }

        // Close modal when clicking outside
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    closeModal();
                }
            });
        }

        // Close modal with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal && modal.classList.contains('show')) {
                closeModal();
            }
        });

        // Initialize all features
        function initializeFeatures() {
            createParticleSystem();
            createMedicalIcons();
            createObserver();
            handleNavbarScroll();
        }

        // Performance-optimized initialization
        window.addEventListener('DOMContentLoaded', () => {
            requestAnimationFrame(() => setTimeout(initializeFeatures, 100));
        });

        // Handle window resize
        window.addEventListener('resize', debounce(() => {
            const particlesContainer = document.getElementById('particles');
            const iconsContainer = document.getElementById('medical-icons');
            
            if (particlesContainer) particlesContainer.innerHTML = '';
            if (iconsContainer) iconsContainer.innerHTML = '';
            
            createParticleSystem();
            createMedicalIcons();
        }, 250));

        // Debounce function
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') document.body.classList.add('keyboard-navigation');
        });
        document.addEventListener('mousedown', () => document.body.classList.remove('keyboard-navigation'));

        // Loading animation
        window.addEventListener('load', () => {
            document.body.style.opacity = '1';
            document.body.style.transform = 'translateY(0)';
        });
 