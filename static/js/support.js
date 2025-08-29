
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

        // Support Tab Switching
        function switchSupportTab(tabName) {
            // Remove active class from all tabs
            document.querySelectorAll('.support-tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Add active class to clicked tab
            event.target.classList.add('active');
            
            // Hide all sections
            document.getElementById('faqSection').style.display = 'none';
            document.getElementById('ticketsSection').style.display = 'none';
            document.getElementById('contactSection').style.display = 'none';
            
            // Show selected section
            if (tabName === 'faq') {
                document.getElementById('faqSection').style.display = 'block';
            } else if (tabName === 'tickets') {
                document.getElementById('ticketsSection').style.display = 'block';
            } else if (tabName === 'contact') {
                document.getElementById('contactSection').style.display = 'block';
            }
        }

        // FAQ Toggle Function
        function toggleFAQ(button) {
            const answer = button.nextElementSibling;
            const chevron = button.querySelector('.chevron-icon');
            const isActive = button.classList.contains('active');
            
            // Close all FAQ items
            document.querySelectorAll('.faq-question').forEach(q => {
                q.classList.remove('active');
                q.nextElementSibling.classList.remove('show');
                q.querySelector('.chevron-icon').classList.remove('rotate');
            });
            
            // If this item wasn't active, open it
            if (!isActive) {
                button.classList.add('active');
                answer.classList.add('show');
                chevron.classList.add('rotate');
            }
        }

        // Search FAQ Function
        function searchFAQ(searchTerm) {
            const faqItems = document.querySelectorAll('.faq-item');
            const searchLower = searchTerm.toLowerCase();
            
            faqItems.forEach(item => {
                const question = item.querySelector('.faq-question').textContent.toLowerCase();
                const answer = item.querySelector('.faq-answer').textContent.toLowerCase();
                
                if (question.includes(searchLower) || answer.includes(searchLower)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = searchTerm === '' ? 'block' : 'none';
                }
            });
        }

        // Support Card Functions
        function startChat() {
            showSuccessMessage('Live chat will be available soon!');
            // In a real app, this would open the chat widget
        }

        function callNow() {
            if (confirm('This will open your phone app to call 1-800-MEDIGENIE. Continue?')) {
                window.open('tel:1-800-6334436');
            }
        }

        function sendEmail() {
            window.open('mailto:support@medigenie.com?subject=Support Request&body=Please describe your issue here...');
        }

        function createTicket() {
            showSuccessMessage('Support ticket creation feature coming soon!');
            // In a real app, this would open a ticket creation modal
        }

        // Show success message
        function showSuccessMessage(message) {
            const successDiv = document.createElement('div');
            successDiv.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #10B981;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
                z-index: 3000;
                font-weight: 500;
                animation: slideInRight 0.3s ease;
            `;
            successDiv.innerHTML = `
                <i class="fas fa-info-circle" style="margin-right: 8px;"></i>
                ${message}
            `;
            
            document.body.appendChild(successDiv);
            
            setTimeout(() => {
                successDiv.remove();
            }, 3000);
        }

        // Logout Function
        function logout() {
            if (confirm('Are you sure you want to logout?')) {
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
            menuButton.style.cssText = 'background: none; border: 1px solid var(--primary-blue); color: var(--primary-blue); padding: 8px 12px; border-radius: 8px;';
            menuButton.onclick = toggleSidebar;
            topNav.insertBefore(menuButton, topNav.firstChild);
        }

        // Add animations with CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100%);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            .faq-answer {
                transition: all 0.3s ease;
            }
            
            .support-card {
                cursor: default;
            }
            
            .support-card:hover .support-icon {
                transform: scale(1.05);
                transition: transform 0.3s ease;
            }
        `;
        document.head.appendChild(style);

        // Notification Bell Click Handler
        document.querySelector('.notification-bell').addEventListener('click', function() {
            alert('You have 2 new notifications:\n1. Support ticket #1234 has been resolved\n2. New FAQ articles available');
        });

        // Initialize page
        document.addEventListener('DOMContentLoaded', function() {
            // Set default active FAQ section
            document.getElementById('faqSection').style.display = 'block';
        });
