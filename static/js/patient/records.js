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

        // File Upload Functions
        function triggerFileInput() {
            document.getElementById('fileInput').click();
        }

        function handleFileUpload(event) {
            const files = event.target.files;
            if (files.length > 0) {
                processFiles(files);
            }
        }

        // Drag and Drop
        const uploadArea = document.getElementById('uploadArea');

        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                processFiles(files);
            }
        });

        // Process uploaded files with OCR simulation
        function processFiles(files) {
            showProcessing();
            
            setTimeout(() => {
                hideProcessing();
                
                // Simulate OCR processing and add records
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    addNewRecord(file);
                }
                
                showSuccessMessage(`${files.length} document(s) processed successfully with OCR!`);
            }, 3000); // Simulate 3 second processing time
        }

        // Add new record to the list
        function addNewRecord(file) {
            const recordsSection = document.querySelector('.records-section');
            const today = new Date().toLocaleDateString();
            
            // Simulate OCR extracted data
            const ocrData = simulateOCR(file.name);
            
            const recordHTML = `
                <div class="record-item" style="border-left: 4px solid var(--primary-blue); animation: slideIn 0.3s ease;">
                    <div class="record-icon icon-${ocrData.type}">
                        <i class="fas fa-${ocrData.icon}"></i>
                    </div>
                    <div class="record-info">
                        <div class="record-title">${ocrData.title}</div>
                        <p class="record-details">${today} • ${ocrData.doctor} • OCR Processed</p>
                    </div>
                    <div class="record-actions">
                        <button class="icon-btn btn-view" title="View" onclick="viewRecord(this)">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="icon-btn btn-download" title="Download" onclick="downloadRecord(this)">
                            <i class="fas fa-download"></i>
                        </button>
                        <button class="icon-btn btn-delete" title="Delete" onclick="deleteRecord(this)">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
            
            recordsSection.insertAdjacentHTML('beforeend', recordHTML);
        }

        // Simulate OCR data extraction
        function simulateOCR(filename) {
            const ocrTemplates = [
                {
                    title: 'Lab Results - Blood Panel',
                    doctor: 'Dr. Sarah Smith',
                    type: 'blood',
                    icon: 'vial'
                },
                {
                    title: 'X-Ray Report - Chest',
                    doctor: 'Dr. Michael Johnson',
                    type: 'xray',
                    icon: 'x-ray'
                },
                {
                    title: 'Prescription Report',
                    doctor: 'Dr. Emily Chen',
                    type: 'prescription',
                    icon: 'prescription-bottle-alt'
                }
            ];
            
            return ocrTemplates[Math.floor(Math.random() * ocrTemplates.length)];
        }

        // Camera Functions
        function openCamera() {
            document.getElementById('cameraModal').style.display = 'flex';
            // In a real app, you would initialize the camera here
            // navigator.mediaDevices.getUserMedia({ video: true })
        }

        function closeCamera() {
            document.getElementById('cameraModal').style.display = 'none';
        }

        function capturePhoto() {
            // Simulate photo capture
            showProcessing();
            closeCamera();
            
            setTimeout(() => {
                hideProcessing();
                
                // Create a simulated captured file
                const simulatedFile = { name: 'captured_report.jpg' };
                addNewRecord(simulatedFile);
                
                showSuccessMessage('Photo captured and processed successfully with OCR!');
            }, 2500);
        }

        // Processing overlay functions
        function showProcessing() {
            document.getElementById('processingOverlay').style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }

        function hideProcessing() {
            document.getElementById('processingOverlay').style.display = 'none';
            document.body.style.overflow = 'auto';
        }

        // Record Actions
        function viewRecord(button) {
            const recordTitle = button.closest('.record-item').querySelector('.record-title').textContent;
            alert(`Viewing: ${recordTitle}\n\nExtracted Data:\n- Patient: John Doe\n- Date: ${new Date().toLocaleDateString()}\n- Key findings extracted via OCR\n\n(Full viewer would open here)`);
        }

        function downloadRecord(button) {
            const recordTitle = button.closest('.record-item').querySelector('.record-title').textContent;
            showSuccessMessage(`Downloading: ${recordTitle}`);
        }

        function deleteRecord(button) {
            const recordItem = button.closest('.record-item');
            const recordTitle = recordItem.querySelector('.record-title').textContent;
            
            if (confirm(`Are you sure you want to delete "${recordTitle}"?`)) {
                recordItem.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {
                    recordItem.remove();
                    showSuccessMessage('Record deleted successfully');
                }, 300);
            }
        }

        // Success message function
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
                max-width: 350px;
            `;
            successDiv.innerHTML = `
                <i class="fas fa-check-circle" style="margin-right: 8px;"></i>
                ${message}
            `;
            
            document.body.appendChild(successDiv);
            
            setTimeout(() => {
                successDiv.remove();
            }, 4000);
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
            alert('Notifications:\n1. New lab results processed\n2. OCR scan completed');
        });

        // Initialize tooltips for better UX
        document.querySelectorAll('[title]').forEach(element => {
            element.addEventListener('mouseenter', function() {
                const tooltip = document.createElement('div');
                tooltip.textContent = this.getAttribute('title');
                tooltip.style.cssText = `
                    position: absolute;
                    background: #333;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-size: 12px;
                    z-index: 1000;
                    pointer-events: none;
                    top: ${this.offsetTop - 35}px;
                    left: ${this.offsetLeft + this.offsetWidth/2}px;
                    transform: translateX(-50%);
                `;
                tooltip.id = 'tooltip';
                document.body.appendChild(tooltip);
            });

            element.addEventListener('mouseleave', function() {
                const tooltip = document.getElementById('tooltip');
                if (tooltip) {
                    tooltip.remove();
                }
            });
        });

        // OCR Information Display
        function showOCRInfo() {
            alert('OCR (Optical Character Recognition) Features:\n\n✓ Automatically extracts text from medical reports\n✓ Identifies key medical data (dates, doctors, diagnoses)\n✓ Supports handwritten and printed documents\n✓ Creates searchable digital records\n✓ Maintains original document integrity\n\nSimply upload an image or take a photo of your report!');
        }

        // Add OCR info button
        document.addEventListener('DOMContentLoaded', function() {
            const uploadSection = document.querySelector('.upload-section');
            const infoButton = document.createElement('button');
            infoButton.innerHTML = '<i class="fas fa-info-circle"></i> How OCR Works';
            infoButton.className = 'action-btn btn-camera';
            infoButton.style.marginTop = '10px';
            infoButton.onclick = showOCRInfo;
            
            const uploadActions = document.querySelector('.upload-actions');
            uploadActions.appendChild(infoButton);
        });

        // File type validation
        function validateFile(file) {
            const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
            const maxSize = 10 * 1024 * 1024; // 10MB
            
            if (!allowedTypes.includes(file.type)) {
                alert('Please upload only JPG, PNG, or PDF files.');
                return false;
            }
            
            if (file.size > maxSize) {
                alert('File size must be less than 10MB.');
                return false;
            }
            
            return true;
        }

        // Enhanced file processing with validation
        function processFiles(files) {
            const validFiles = [];
            
            for (let file of files) {
                if (validateFile(file)) {
                    validFiles.push(file);
                }
            }
            
            if (validFiles.length === 0) {
                return;
            }
            
            showProcessing();
            
            setTimeout(() => {
                hideProcessing();
                
                validFiles.forEach(file => {
                    addNewRecord(file);
                });
                
                showSuccessMessage(`${validFiles.length} document(s) processed successfully with OCR!`);
                
                // Reset file input
                document.getElementById('fileInput').value = '';
            }, 3000);
        }
