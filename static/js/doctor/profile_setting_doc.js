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
            
            // Default to profile if no match found
            if (!document.querySelector('.nav-item.active') && currentPage.includes('profile')) {
                document.getElementById('profile-link').classList.add('active');
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

        // Tab switching functionality
        function switchTab(tabName) {
            // Remove active class from all tab buttons
            const tabButtons = document.querySelectorAll('.tab-btn');
            tabButtons.forEach(button => {
                button.classList.remove('active');
            });

            // Remove active class from all tab panels
            const tabPanels = document.querySelectorAll('.tab-panel');
            tabPanels.forEach(panel => {
                panel.classList.remove('active');
            });

            // Add active class to clicked tab button
            event.target.classList.add('active');

            // Show corresponding tab panel
            const targetPanel = document.getElementById(tabName + '-tab');
            if (targetPanel) {
                targetPanel.classList.add('active');
            }
        }

        // Toggle functionality for availability
        document.addEventListener('DOMContentLoaded', function() {
            const toggleInputs = document.querySelectorAll('.toggle-input');
            
            toggleInputs.forEach(toggle => {
                toggle.addEventListener('change', function() {
                    const daySchedule = this.closest('.day-schedule');
                    const timeInputs = daySchedule ? daySchedule.querySelectorAll('.time-input') : [];
                    const statusElement = daySchedule ? daySchedule.querySelector('.availability-status span') : null;
                    
                    if (daySchedule && timeInputs.length > 0 && statusElement) {
                        if (this.checked) {
                            // Enable time inputs
                            timeInputs.forEach(input => {
                                input.disabled = false;
                            });
                            // Update status
                            statusElement.textContent = 'Available';
                            statusElement.className = 'status-available';
                        } else {
                            // Disable time inputs
                            timeInputs.forEach(input => {
                                input.disabled = true;
                            });
                            // Update status
                            statusElement.textContent = 'Not Available';
                            statusElement.className = 'status-unavailable';
                        }
                    }
                });
            });

            // Set initial state for disabled days (Saturday, Sunday)
            const daySchedules = document.querySelectorAll('.day-schedule');
            daySchedules.forEach((daySchedule, index) => {
                const toggle = daySchedule.querySelector('.toggle-input');
                const timeInputs = daySchedule.querySelectorAll('.time-input');
                
                if (toggle && !toggle.checked) {
                    timeInputs.forEach(input => input.disabled = true);
                }
            });
        });

        // Save button functionality
        document.querySelectorAll('.save-btn').forEach(button => {
            button.addEventListener('click', function() {
                // Show loading state
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
                this.disabled = true;
                
                // Simulate save delay
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-check"></i> Saved';
                    
                    // Reset after 2 seconds
                    setTimeout(() => {
                        this.innerHTML = '<i class="fas fa-save"></i> Save Changes';
                        this.disabled = false;
                    }, 2000);
                }, 1000);
            });
        });

        // File upload functionality
        document.querySelector('.upload-btn').addEventListener('click', function() {
            // Create invisible file input
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*';
            fileInput.style.display = 'none';
            
            fileInput.addEventListener('change', function(e) {
                if (e.target.files[0]) {
                    // Here you would normally upload the file
                    console.log('File selected:', e.target.files[0]);
                    alert('Profile photo uploaded successfully!');
                }
            });
            
            document.body.appendChild(fileInput);
            fileInput.click();
            document.body.removeChild(fileInput);
        });