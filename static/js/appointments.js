           let selectedTimeSlot = null;
        let appointments = [];

        // Initialize date picker with today's date as minimum
        document.addEventListener('DOMContentLoaded', function() {
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('appointmentDate').min = today;
        });

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

        // Tab Switching
        function switchTab(tabName) {
            // Remove active class from all tabs
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Add active class to clicked tab
            event.target.classList.add('active');
            
            // Update content based on tab
            const grid = document.getElementById('appointmentsGrid');
            if (tabName === 'past') {
                grid.innerHTML = '<div style="text-align: center; padding: 40px; color: #6B7280;"><i class="far fa-calendar-alt" style="font-size: 48px; margin-bottom: 15px; display: block;"></i><h4>No Past Appointments</h4><p>You have no appointment history to display.</p></div>';
            } else if (tabName === 'book') {
                openBookingModal();
            } else {
                // Show upcoming appointments (default content)
                location.reload();
            }
        }

        // Booking Modal Functions
        function openBookingModal() {
            document.getElementById('bookingModal').style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }

        function closeBookingModal() {
            document.getElementById('bookingModal').style.display = 'none';
            document.body.style.overflow = 'auto';
            resetBookingForm();
        }

        function resetBookingForm() {
            document.getElementById('bookingForm').reset();
            document.getElementById('specialtyField').value = '';
            selectedTimeSlot = null;
            document.querySelectorAll('.time-slot').forEach(slot => {
                slot.classList.remove('selected');
            });
        }

        // Update specialty field when doctor is selected
        function updateSpecialty() {
            const doctorSelect = document.getElementById('doctorSelect');
            const specialtyField = document.getElementById('specialtyField');
            
            if (doctorSelect.value) {
                const specialty = doctorSelect.value.split('|')[1];
                specialtyField.value = specialty;
            } else {
                specialtyField.value = '';
            }
        }

        // Time slot selection
        function selectTimeSlot(element) {
            // Remove selection from all slots
            document.querySelectorAll('.time-slot').forEach(slot => {
                slot.classList.remove('selected');
            });
            
            // Select clicked slot
            element.classList.add('selected');
            selectedTimeSlot = element.dataset.time;
        }

        // Form submission
        document.getElementById('bookingForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const doctorSelect = document.getElementById('doctorSelect');
            const appointmentDate = document.getElementById('appointmentDate');
            const appointmentType = document.getElementById('appointmentType');
            
            // Validation
            if (!doctorSelect.value) {
                alert('Please select a doctor');
                return;
            }
            
            if (!appointmentDate.value) {
                alert('Please select an appointment date');
                return;
            }
            
            if (!selectedTimeSlot) {
                alert('Please select a time slot');
                return;
            }
            
            // Create new appointment
            const doctorInfo = doctorSelect.value.split('|');
            const doctorName = doctorInfo[0];
            const specialty = doctorInfo[1];
            
            // Format date
            const dateObj = new Date(appointmentDate.value);
            const formattedDate = (dateObj.getMonth() + 1) + '/' + dateObj.getDate() + '/' + dateObj.getFullYear();
            
            // Create appointment card
            const appointmentCard = createAppointmentCard({
                doctorName: doctorName,
                specialty: specialty,
                date: formattedDate,
                time: selectedTimeSlot + ' (30 min)',
                location: 'Room TBD, Main Building',
                status: 'pending',
                type: appointmentType.value.charAt(0).toUpperCase() + appointmentType.value.slice(1)
            });
            
            // Add to appointments grid
            const grid = document.getElementById('appointmentsGrid');
            grid.insertAdjacentHTML('afterbegin', appointmentCard);
            
            // Close modal and show success message
            closeBookingModal();
            showSuccessMessage('Appointment booked successfully!');
        });

        // Create appointment card HTML
        function createAppointmentCard(appointment) {
            const initials = appointment.doctorName.split(' ').map(n => n[0]).join('');
            const statusClass = appointment.status === 'confirmed' ? 'status-confirmed' : 'status-pending';
            
            return `
                <div class="appointment-card" style="border-left: 4px solid var(--primary-blue); animation: slideIn 0.3s ease;">
                    <div class="appointment-header">
                        <div class="doctor-avatar">${initials}</div>
                        <div class="doctor-info">
                            <h3 class="doctor-name">${appointment.doctorName}</h3>
                            <p class="doctor-specialty">${appointment.specialty}</p>
                        </div>
                        <div class="appointment-status ${statusClass}">${appointment.status}</div>
                    </div>
                    
                    <div class="appointment-details">
                        <div class="detail-item">
                            <i class="far fa-calendar detail-icon"></i>
                            <span>${appointment.date}</span>
                        </div>
                        <div class="detail-item">
                            <i class="far fa-clock detail-icon"></i>
                            <span>${appointment.time}</span>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-map-marker-alt detail-icon"></i>
                            <span>${appointment.location}</span>
                        </div>
                    </div>
                    
                    <div class="appointment-actions">
                        <button class="action-btn btn-reschedule" onclick="rescheduleAppointment(this)">Reschedule</button>
                        <button class="action-btn btn-cancel" onclick="cancelAppointment(this)">Cancel</button>
                        <span class="appointment-type">${appointment.type}</span>
                    </div>
                </div>
            `;
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
                <i class="fas fa-check-circle" style="margin-right: 8px;"></i>
                ${message}
            `;
            
            document.body.appendChild(successDiv);
            
            setTimeout(() => {
                successDiv.remove();
            }, 3000);
        }

        // Reschedule appointment
        function rescheduleAppointment(button) {
            if (confirm('Are you sure you want to reschedule this appointment?')) {
                // In a real app, this would open a reschedule modal
                alert('Reschedule functionality will be implemented');
            }
        }

        // Cancel appointment
        function cancelAppointment(button) {
            if (confirm('Are you sure you want to cancel this appointment?')) {
                const appointmentCard = button.closest('.appointment-card');
                appointmentCard.style.animation = 'slideOut 0.3s ease';
                
                setTimeout(() => {
                    appointmentCard.remove();
                    showSuccessMessage('Appointment cancelled successfully');
                }, 300);
            }
        }

        // Search functionality
        document.querySelector('.search-input').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const appointmentCards = document.querySelectorAll('.appointment-card');
            
            appointmentCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });

        // Filter by specialty
        document.querySelector('.filter-select').addEventListener('change', function(e) {
            const selectedSpecialty = e.target.value;
            const appointmentCards = document.querySelectorAll('.appointment-card');
            
            if (selectedSpecialty === 'Filter by specialty') {
                appointmentCards.forEach(card => {
                    card.style.display = 'block';
                });
            } else {
                appointmentCards.forEach(card => {
                    const specialty = card.querySelector('.doctor-specialty').textContent;
                    if (specialty === selectedSpecialty) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            }
        });

        // Close modal when clicking outside
        document.getElementById('bookingModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeBookingModal();
            }
        });

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
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideOut {
                from {
                    opacity: 1;
                    transform: translateX(0);
                }
                to {
                    opacity: 0;
                    transform: translateX(-100%);
                }
            }
            
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
        `;
        document.head.appendChild(style);

        // Notification Bell Click Handler
        document.querySelector('.notification-bell').addEventListener('click', function() {
            alert('You have 2 new notifications:\n1. Appointment confirmed with Dr. Smith\n2. Lab results are ready');
        });

        // Auto-refresh appointments every 30 seconds (placeholder)
        setInterval(function() {
            console.log('Auto-refreshing appointments...');
            // In a real app, this would make an API call to refresh appointments
        }, 30000);
