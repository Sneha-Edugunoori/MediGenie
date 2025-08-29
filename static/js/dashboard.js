        // Profile Dropdown Toggle
        function toggleProfileDropdown() {
            const dropdown = document.getElementById('profileDropdown');
            dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
        }

        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            const dropdown = document.getElementById('profileDropdown');
            const profileBtn = document.querySelector('.profile-btn');
            
            if (!profileBtn.contains(event.target)) {
                dropdown.style.display = 'none';
            }
        });

        // Quick Action Functions
        function bookAppointment() {
            window.location.href = '/appointments';
        }

        function viewMedicalRecords() {
            window.location.href = '/medical-records';
        }

        function viewMessages() {
            window.location.href = '/communication';
        }

        function viewHealthTracking() {
            window.location.href = '/health-tracking';
        }

        // Logout Function
        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                // Add logout logic here
                alert('Logout functionality will be implemented');
            }
        }

        // Mobile Sidebar Toggle
        function toggleSidebar() {
            const sidebar = document.querySelector('.sidebar');
            sidebar.classList.toggle('open');
        }

        // Add mobile menu button for responsive design
        if (window.innerWidth <= 768) {
            const topNav = document.querySelector('.top-nav');
            const menuButton = document.createElement('button');
            menuButton.innerHTML = '<i class="fas fa-bars"></i>';
            menuButton.className = 'btn btn-outline-primary me-3';
            menuButton.onclick = toggleSidebar;
            topNav.insertBefore(menuButton, topNav.firstChild);
        }

        // Sidebar Active Link Management
        document.addEventListener('DOMContentLoaded', function() {
            const currentPath = window.location.pathname;
            const sidebarLinks = document.querySelectorAll('.sidebar-menu .nav-link');
            
            sidebarLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === currentPath || 
                    (currentPath === '/' && link.getAttribute('href') === '/dashboard')) {
                    link.classList.add('active');
                }
            });
        });

        // Smooth Scrolling for Better UX
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });

        // Add Loading States for Better UX
        function showLoading(element) {
            const originalText = element.innerHTML;
            element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
            element.disabled = true;
            
            setTimeout(() => {
                element.innerHTML = originalText;
                element.disabled = false;
            }, 1000);
        }

        // Add click handlers for cards with loading states
        document.querySelectorAll('.action-card').forEach(card => {
            card.addEventListener('click', function() {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });

        // Notification Bell Click Handler
        document.querySelector('.notification-bell').addEventListener('click', function() {
            alert('Notifications feature will be implemented');
        });

        // Health Metrics Click Handlers
        document.querySelectorAll('.health-metric').forEach(metric => {
            metric.style.cursor = 'pointer';
            metric.addEventListener('click', function() {
                alert('Detailed health metrics view will be implemented');
            });
        });

        // Auto-refresh data every 5 minutes (placeholder)
        setInterval(function() {
            console.log('Auto-refreshing dashboard data...');
            // Add API calls to refresh data here
        }, 300000); // 5 minutes
