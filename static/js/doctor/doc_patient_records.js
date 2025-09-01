// Set active navigation item based on current page
        document.addEventListener('DOMContentLoaded', function() {
            const currentPage = window.location.pathname.split('/').pop();
            const navItems = document.querySelectorAll('.nav-item');
            
            // Remove active class from all items
            navItems.forEach(item => {
                item.classList.remove('active');
            });
            
            // Add active class to current page
            navItems.forEach(item => {
                if (item.getAttribute('href') === currentPage) {
                    item.classList.add('active');
                }
            });
            
            // Default to dashboard if no match found
            if (!document.querySelector('.nav-item.active') && currentPage.includes('doctor')) {
                document.getElementById('dashboard-link').classList.add('active');
            }
        });

        // Handle navigation clicks
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', function(e) {
                // Remove active from all items
                document.querySelectorAll('.nav-item').forEach(nav => {
                    nav.classList.remove('active');
                });
                
                // Add active to clicked item
                this.classList.add('active');
            });
        });

        // Function to set active page (call this from individual pages)
        function setActivePage(pageId) {
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(item => {
                item.classList.remove('active');
            });
            
            const activeItem = document.getElementById(pageId);
            if (activeItem) {
                activeItem.classList.add('active');
            }
        }

        // Make function globally available
        window.setActivePage = setActivePage;