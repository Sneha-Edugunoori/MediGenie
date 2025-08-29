        // Tab functionality
        function showTab(tabId) {
            // Hide all tab panes
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('active');
            });
            
            // Remove active class from all tab buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab pane
            document.getElementById(tabId).classList.add('active');
            
            // Add active class to clicked button
            event.target.classList.add('active');
        }

        // Show Add Vitals tab when Add Entry button is clicked
        function showAddVitalsTab() {
            showTab('add-vitals');
            document.querySelector('.tab-btn').classList.add('active');
        }

        // Save vitals function
        function saveVitals(event) {
            event.preventDefault();
            
            const button = event.target.querySelector('.save-btn');
            const originalText = button.innerHTML;
            
            // Show loading state
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
            button.disabled = true;
            
            // Simulate API call
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-check"></i> Saved Successfully!';
                // button.style.background = var('--success-green');
                // button.style.background = "#22c55e"; // Tailwind's green-500 for example

                
                // Reset button after 2 seconds
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.disabled = false;
                    button.style.background = '';
                    
                    // Reset form
                    event.target.reset();
                    
                    // Show success message
                    alert('Vital signs saved successfully!');
                }, 2000);
            }, 1000);
        }

        // Logout function
        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                alert('Logout functionality will be implemented');
            }
        }

        // Mobile sidebar toggle
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

        // Notification bell click handler
        document.querySelector('.notification-bell').addEventListener('click', function() {
            alert('You have 2 new notifications:\n• Lab results are ready\n• Appointment reminder for tomorrow');
        });

        // Add hover effects for metric cards
        document.querySelectorAll('.metric-card').forEach(card => {
            card.addEventListener('click', function() {
                const title = this.querySelector('.metric-title').textContent;
                alert(`Detailed view for ${title} will be implemented`);
            });
        });

        // Form validation
        document.querySelectorAll('input[type="number"]').forEach(input => {
            input.addEventListener('input', function() {
                if (this.value && (this.value < this.min || this.value > this.max)) {
                    this.style.borderColor = '#EF4444';
                } else {
                    this.style.borderColor = '';
                }
            });
        });
