 // Set active navigation item - Appointments is active for this page
        document.addEventListener('DOMContentLoaded', function() {
            // Make sure appointments link is active
            document.getElementById('appointments-link').classList.add('active');
            
            // Handle navigation clicks
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(item => {
                item.addEventListener('click', function(e) {
                    navItems.forEach(nav => nav.classList.remove('active'));
                    this.classList.add('active');
                });
            });

            // Tab functionality
            const tabBtns = document.querySelectorAll('.tab-btn');
            const tabContents = document.querySelectorAll('.tab-content');

            tabBtns.forEach(btn => {
                btn.addEventListener('click', function() {
                    const targetTab = this.getAttribute('data-tab');
                    tabBtns.forEach(b => b.classList.remove('active'));
                    tabContents.forEach(c => c.classList.remove('active'));
                    this.classList.add('active');
                    document.getElementById(targetTab + '-tab').classList.add('active');
                });
            });

            // Calendar navigation
            const prevBtn = document.getElementById('prev-month');
            const nextBtn = document.getElementById('next-month');
            const currentMonthEl = document.getElementById('current-month');
            const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            let currentMonth = 7; // August
            let currentYear = 2025;

            function updateCalendar() {
                currentMonthEl.textContent = `${months[currentMonth]} ${currentYear}`;
            }

            prevBtn.addEventListener('click', function() {
                currentMonth--;
                if (currentMonth < 0) {
                    currentMonth = 11;
                    currentYear--;
                }
                updateCalendar();
            });

            nextBtn.addEventListener('click', function() {
                currentMonth++;
                if (currentMonth > 11) {
                    currentMonth = 0;
                    currentYear++;
                }
                updateCalendar();
            });

            // Appointment interactions
            document.querySelectorAll('.appointment-slot').forEach(slot => {
                slot.addEventListener('click', function(e) {
                    e.stopPropagation();
                    alert('Appointment: ' + this.textContent);
                });
            });

            document.querySelectorAll('.calendar-day').forEach(day => {
                day.addEventListener('click', function() {
                    const dayNumber = this.querySelector('.day-number').textContent;
                    if (!this.querySelector('.day-number').classList.contains('other-month')) {
                        alert(`Add appointment for ${months[currentMonth]} ${dayNumber}, ${currentYear}`);
                    }
                });
            });

            // Request actions
            document.querySelectorAll('.accept-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    this.textContent = 'Accepted';
                    this.style.background = '#22c55e';
                    this.disabled = true;
                    const rejectBtn = this.parentNode.querySelector('.reject-btn');
                    if (rejectBtn) rejectBtn.style.display = 'none';
                });
            });

            document.querySelectorAll('.reject-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    if (confirm('Reject this appointment?')) {
                        this.closest('.request-card').style.opacity = '0.5';
                        this.textContent = 'Rejected';
                        this.disabled = true;
                        const acceptBtn = this.parentNode.querySelector('.accept-btn');
                        if (acceptBtn) acceptBtn.style.display = 'none';
                    }
                });
            });

            // Search functionality
            document.querySelectorAll('.search-input').forEach(input => {
                input.addEventListener('input', function() {
                    const searchTerm = this.value.toLowerCase();
                    const cards = this.closest('.tab-content').querySelectorAll('.request-card');
                    cards.forEach(card => {
                        const patientName = card.querySelector('h3').textContent.toLowerCase();
                        card.style.display = patientName.includes(searchTerm) ? 'block' : 'none';
                    });
                });
            });
        });