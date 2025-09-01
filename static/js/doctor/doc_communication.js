// Tab switching functionality
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                
                // Remove active class from all tabs and content
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked tab and corresponding content
                button.classList.add('active');
                document.getElementById(`${targetTab}-content`).classList.add('active');
            });
        });

        // Message item click functionality
        const messageItems = document.querySelectorAll('.message-item');
        const chatPatientAvatar = document.querySelector('.chat-patient-avatar');
        const chatPatientName = document.querySelector('.chat-patient-details h4');
        const chatPatientInfo = document.querySelector('.chat-patient-details p');

        // Patient data
        const patientData = {
            sarah: {
                name: 'Sarah Johnson',
                avatar: 'SJ',
                info: 'Patient ID: #12345 • Last seen: 2 days ago',
                gradient: 'linear-gradient(135deg, #60a5fa, #3b82f6)'
            },
            mike: {
                name: 'Mike Chen',
                avatar: 'MC',
                info: 'Patient ID: #12346 • Last seen: 1 week ago',
                gradient: 'linear-gradient(135deg, #fb923c, #f97316)'
            },
            emma: {
                name: 'Emma Davis',
                avatar: 'ED',
                info: 'Patient ID: #12347 • Last seen: 3 days ago',
                gradient: 'linear-gradient(135deg, #a78bfa, #8b5cf6)'
            },
            john: {
                name: 'John Smith',
                avatar: 'JS',
                info: 'Patient ID: #12348 • Last seen: 1 week ago',
                gradient: 'linear-gradient(135deg, #22c55e, #16a34a)'
            },
            lisa: {
                name: 'Lisa Wilson',
                avatar: 'LW',
                info: 'Patient ID: #12349 • Last seen: 2 weeks ago',
                gradient: 'linear-gradient(135deg, #f59e0b, #d97706)'
            },
            robert: {
                name: 'Robert Brown',
                avatar: 'RB',
                info: 'Patient ID: #12350 • Last seen: 1 month ago',
                gradient: 'linear-gradient(135deg, #ef4444, #dc2626)'
            }
        };

        messageItems.forEach(item => {
            item.addEventListener('click', () => {
                // Remove active class from all items
                messageItems.forEach(msg => msg.classList.remove('active'));
                
                // Add active class to clicked item
                item.classList.add('active');
                
                // Get patient data
                const patientKey = item.getAttribute('data-patient');
                const patient = patientData[patientKey];
                
                if (patient) {
                    chatPatientAvatar.textContent = patient.avatar;
                    chatPatientAvatar.style.background = patient.gradient;
                    chatPatientName.textContent = patient.name;
                    chatPatientInfo.textContent = patient.info;
                }
            });
        });

        // Chat input auto-resize
        const chatInput = document.querySelector('.chat-input-field');
        const sendButton = document.querySelector('.send-btn');

        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 100) + 'px';
            
            // Enable/disable send button based on input
            sendButton.disabled = this.value.trim() === '';
        });

        // Send message functionality
        function sendMessage() {
            const message = chatInput.value.trim();
            if (message === '') return;
            
            const chatMessages = document.querySelector('.chat-messages');
            const messageElement = document.createElement('div');
            messageElement.className = 'message sent';
            
            const currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            messageElement.innerHTML = `
                <div class="message-bubble">
                    ${message}
                    <div class="message-timestamp">Today, ${currentTime}</div>
                </div>
            `;
            
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Clear input
            chatInput.value = '';
            chatInput.style.height = 'auto';
            sendButton.disabled = true;
        }

        sendButton.addEventListener('click', sendMessage);

        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Initialize send button state
        sendButton.disabled = true;

        // Search functionality
        const searchInput = document.querySelector('.search-box input');
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            messageItems.forEach(item => {
                const patientName = item.querySelector('h4').textContent.toLowerCase();
                const messagePreview = item.querySelector('.message-preview').textContent.toLowerCase();
                
                if (patientName.includes(searchTerm) || messagePreview.includes(searchTerm)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });

        // Video call button functionality
        document.addEventListener('click', function(e) {
            if (e.target.closest('.consult-btn.btn-primary')) {
                const button = e.target.closest('.consult-btn.btn-primary');
                const card = button.closest('.consultation-card');
                const patientName = card.querySelector('.consultation-info h4').textContent;
                
                // Simulate starting/joining video call
                alert(`Starting video consultation with ${patientName}...`);
            }
        });

        // Action buttons in chat header
        document.addEventListener('click', function(e) {
            if (e.target.closest('.action-btn.video')) {
                const patientName = chatPatientName.textContent;
                alert(`Starting video call with ${patientName}...`);
            } else if (e.target.closest('.action-btn') && e.target.closest('.action-btn').textContent.includes('Call')) {
                const patientName = chatPatientName.textContent;
                alert(`Calling ${patientName}...`);
            } else if (e.target.closest('.action-btn') && e.target.closest('.action-btn').textContent.includes('Records')) {
                const patientName = chatPatientName.textContent;
                alert(`Opening medical records for ${patientName}...`);
            }
        });s