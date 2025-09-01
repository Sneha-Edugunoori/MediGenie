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
            
            // Default to prescriptions if no match found
            if (!document.querySelector('.nav-item.active')) {
                document.getElementById('prescription-link').classList.add('active');
            }

            // Initialize speech recognition
            initSpeechRecognition();
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

        // Voice recognition variables
        let recognition = null;
        let isListening = false;

        // Initialize speech recognition if available
        function initSpeechRecognition() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'en-US';

                recognition.onstart = function() {
                    isListening = true;
                    updateVoiceStatus('listening', 'Listening...');
                    document.getElementById('voiceBtn').classList.add('listening');
                };

                recognition.onresult = function(event) {
                    let finalTranscript = '';
                    let interimTranscript = '';

                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        const transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {
                            finalTranscript += transcript;
                        } else {
                            interimTranscript += transcript;
                        }
                    }

                    const prescriptionTextarea = document.getElementById('prescriptionText');
                    const currentText = prescriptionTextarea.value;
                    
                    if (finalTranscript) {
                        if (currentText && !currentText.endsWith(' ') && !currentText.endsWith('\n')) {
                            prescriptionTextarea.value = currentText + ' ' + finalTranscript;
                        } else {
                            prescriptionTextarea.value = currentText + finalTranscript;
                        }
                    }
                };

                recognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                    updateVoiceStatus('error', `Error: ${event.error}`);
                    stopVoiceInput();
                };

                recognition.onend = function() {
                    if (isListening) {
                        updateVoiceStatus('stopped', 'Voice input stopped');
                        setTimeout(() => {
                            hideVoiceStatus();
                        }, 2000);
                    }
                    stopVoiceInput();
                };
            }
        }

        function toggleVoiceInput() {
            if (!recognition) {
                alert('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
                return;
            }

            if (isListening) {
                stopVoiceInput();
            } else {
                startVoiceInput();
            }
        }

        function startVoiceInput() {
            if (recognition && !isListening) {
                try {
                    recognition.start();
                } catch (error) {
                    console.error('Error starting speech recognition:', error);
                    alert('Could not start voice input. Please try again.');
                }
            }
        }

        function stopVoiceInput() {
            if (recognition && isListening) {
                isListening = false;
                recognition.stop();
                document.getElementById('voiceBtn').classList.remove('listening');
            }
        }

        function updateVoiceStatus(type, message) {
            const statusElement = document.getElementById('voiceStatus');
            statusElement.textContent = message;
            statusElement.className = `voice-status show ${type}`;
        }

        function hideVoiceStatus() {
            const statusElement = document.getElementById('voiceStatus');
            statusElement.classList.remove('show');
        }

        // Modal functions
        function openPrescriptionModal() {
            document.getElementById('prescriptionModal').style.display = 'flex';
            document.getElementById('modalTitle').textContent = 'Create New Prescription';
            document.getElementById('prescriptionForm').reset();
            hideVoiceStatus();
        }

        function closePrescriptionModal() {
            document.getElementById('prescriptionModal').style.display = 'none';
            stopVoiceInput();
            hideVoiceStatus();
        }

        function editPrescription(patientId) {
            document.getElementById('prescriptionModal').style.display = 'flex';
            document.getElementById('modalTitle').textContent = 'Edit Prescription';
            
            if (patientId === 'sarah-johnson') {
                document.getElementById('patientSelect').value = 'sarah-johnson';
                document.getElementById('diagnosis').value = 'Hypertension';
                document.getElementById('prescriptionText').value = `Medication: Lisinopril 10mg
Dosage: Once daily
Duration: 30 days
Instructions: Take in the morning with or without food

Medication: Hydrochlorothiazide 25mg  
Dosage: Once daily
Duration: 30 days
Instructions: Take in the morning, may cause increased urination`;
                document.getElementById('refills').value = '2';
            } else if (patientId === 'mike-chen') {
                document.getElementById('patientSelect').value = 'mike-chen';
                document.getElementById('diagnosis').value = 'Diabetes Type 2';
                document.getElementById('prescriptionText').value = `Medication: Metformin 500mg
Dosage: Twice daily
Duration: 60 days
Instructions: Take with meals to reduce stomach upset

Medication: Glimepiride 2mg
Dosage: Once daily
Duration: 60 days
Instructions: Take 30 minutes before breakfast`;
                document.getElementById('refills').value = '1';
            }
        }

        function savePrescription() {
            const form = document.getElementById('prescriptionForm');
            const formData = new FormData(form);
            
            if (!formData.get('patient') || !formData.get('prescriptionText')) {
                alert('Please fill in all required fields.');
                return;
            }

            alert('Prescription saved successfully!');
            closePrescriptionModal();
            
            console.log('Prescription data:', Object.fromEntries(formData));
        }

        // Close modal when clicking outside
        document.getElementById('prescriptionModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closePrescriptionModal();
            }
        });

        // Close modal on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && document.getElementById('prescriptionModal').style.display === 'flex') {
                closePrescriptionModal();
            }
        });