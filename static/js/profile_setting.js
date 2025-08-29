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

        // Edit photo function
        function editPhoto() {
            alert('Photo editing functionality will be implemented');
        }

        // Save functions
        function savePersonalInfo(event) {
            event.preventDefault();
            showSuccessMessage(event.target.querySelector('.save-btn'));
        }

        function saveMedicalInfo(event) {
            event.preventDefault();
            showSuccessMessage(event.target.querySelector('.save-btn'));
        }

        function saveNotifications() {
            showSuccessMessage(event.target);
        }

        function changePassword(event) {
            event.preventDefault();
            const newPass = event.target.querySelector('input[placeholder="Enter new password"]').value;
            const confirmPass = event.target.querySelector('input[placeholder="Confirm new password"]').value;
            
            if (newPass !== confirmPass) {
                alert('Passwords do not match!');
                return;
            }
            
            showSuccessMessage(event.target.querySelector('.save-btn'));
            event.target.reset();
        }

        // Show success message
        function showSuccessMessage(button) {
            const originalText = button.innerHTML;
            
            button.innerHTML = '<i class="fas fa-check"></i> Saved!';
            button.style.background = '#10B981';
            button.disabled = true;
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.style.background = '';
                button.disabled = false;
            }, 2000);
        }

        // Logout function
        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                alert('Logout functionality will be implemented');
            }
        }

        // Initialize page
        document.addEventListener('DOMContentLoaded', function() {
            // Notification bell click handler
            document.querySelector('.notification-bell').addEventListener('click', function() {
                alert('You have 2 new notifications:\n• Lab results are ready\n• Appointment reminder for tomorrow');
            });

            // Toggle switch functionality
            document.querySelectorAll('.toggle-switch input').forEach(toggle => {
                toggle.addEventListener('change', function() {
                    const parent = this.closest('.notification-item');
                    if (parent) {
                        const info = parent.querySelector('.notification-info h6').textContent;
                        console.log(`${info} notification ${this.checked ? 'enabled' : 'disabled'}`);
                    }
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
        });

        // Mobile sidebar toggle
        function toggleSidebar() {
            const sidebar = document.querySelector('.sidebar');
            sidebar.classList.toggle('open');
        }

        // Add mobile menu button for responsive design
        if (window.innerWidth <= 768) {
            window.addEventListener('load', function() {
                const topNav = document.querySelector('.top-nav');
                const menuButton = document.createElement('button');
                menuButton.innerHTML = '<i class="fas fa-bars"></i>';
                menuButton.className = 'btn btn-outline-primary me-3';
                menuButton.onclick = toggleSidebar;
                topNav.insertBefore(menuButton, topNav.firstChild);
            });
        }
