// scripts.js

/* Wait for the DOM to load */
document.addEventListener('DOMContentLoaded', () => {
    /* Responsive Navigation Menu */
    const menuIcon = document.querySelector('.menu-icon');
    const navLinks = document.querySelector('.nav-links');

    window.toggleMenu = function() {
        navLinks.classList.toggle('active');
    }

    /* Tabs Functionality */
    window.openTab = function(evt, tabName) {
        // Hide all tab contents
        const tabContents = document.querySelectorAll('.tab-content');
        tabContents.forEach(content => content.classList.remove('active'));

        // Remove active class from all tab buttons
        const tabLinks = document.querySelectorAll('.tablinks');
        tabLinks.forEach(link => link.classList.remove('active'));

        // Show current tab
        const activeTab = document.getElementById(tabName);
        activeTab.classList.add('active');

        // Add active class to the clicked tab
        evt.currentTarget.classList.add('active');

        // Smooth scroll to the active tab
        activeTab.scrollIntoView({ behavior: 'smooth' });
    }

    /* Dark Mode Toggle */
    window.toggleDarkMode = function() {
        document.body.classList.toggle(\"dark-mode\");
        const button = document.querySelector('.dark-mode-toggle');
        button.textContent = document.body.classList.contains(\"dark-mode\") ? \" Light Mode\" : \" Dark Mode\";
    }

    /* Theme Customization */
    window.changeTheme = function(theme) {
        document.body.classList.remove('forest-theme', 'ocean-theme', 'sunset-theme');
        if (theme !== 'default') {
            document.body.classList.add(${theme}-theme);
        }
        showToast(${theme.charAt(0).toUpperCase() + theme.slice(1)} theme applied.);
    }

    /* Toast Notification */
    window.showToast = function(message) {
        const toast = document.createElement('div');
        toast.classList.add('toast');
        toast.textContent = message;
        document.getElementById('toast-container').appendChild(toast);
        setTimeout(() => {
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
                toast.remove();
            }, 3000);
        }, 100);
    }

    /* Initialize Particles.js */
    window.initParticles = function() {
        particlesJS(\"particles-js\", {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: [\"#8B4513\", \"#C0C0C0\", \"#228B22\", \"#ffffff\", \"#654321\"] },
                shape: { type: \"circle\" },
                opacity: { value: 0.6, random: true },
                size: { value: 4, random: true },
                line_linked: { enable: false },
                move: { 
                    enable: true, 
                    speed: 3, 
                    direction: \"none\", 
                    random: true, 
                    straight: false, 
                    out_mode: \"out\",
                    attract: {
                        enable: false,
                        rotateX: 600,
                        rotateY: 1200
                    }
                }
            },
            interactivity: {
                detect_on: \"canvas\",
                events: {
                    onhover: { enable: true, mode: \"repulse\" },
                    onclick: { enable: true, mode: \"push\" },
                    resize: true
                },
                modes: {
                    repulse: { distance: 100, duration: 0.4 },
                    push: { particles_nb: 4 }
                }
            },
            retina_detect: true
        });
    }

    /* Initialize Lazy Loading for Images */
    window.initLazyLoading = function() {
        const lazyImages = document.querySelectorAll('img.gallery-img');

        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: \"0px 0px 50px 0px\",
            threshold: 0.01
        });

        lazyImages.forEach(img => {
            img.dataset.src = img.src;
            img.src = 'https://via.placeholder.com/10x10?text=Loading'; // Low-res placeholder
            imageObserver.observe(img);
        });
    }

    /* Initialize All Modules */
    window.initAll = function() {
        initParticles();
        initLazyLoading();
    }

    /* Call initAll on DOMContentLoaded */
    initAll();
