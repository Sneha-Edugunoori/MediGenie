        // Set active navigation item based on current page
        document.addEventListener('DOMContentLoaded', function() {
            const currentPage = window.location.pathname.split('/').pop();
            const navItems = document.querySelectorAll('.nav-item');
            
            // Remove active class from all items
            navItems.forEach(item => {
                item.classList.remove('active');
            });
            
            // Add active class to current page or default to dashboard
            if (currentPage.includes('dashboard') || currentPage === '' || currentPage === 'analytics.html') {
                document.getElementById('dashboard-link').classList.add('active');
            }
            
            // Handle navigation clicks
            navItems.forEach(item => {
                item.addEventListener('click', function(e) {
                    // Remove active from all items
                    document.querySelectorAll('.nav-item').forEach(nav => {
                        nav.classList.remove('active');
                    });
                    
                    // Add active to clicked item
                    this.classList.add('active');
                });
            });
        });
