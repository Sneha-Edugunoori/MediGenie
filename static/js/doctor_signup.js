        function goBack() {
            // You can customize this to go to your main page
            window.history.back();
        }

        function validateForm() {
            let isValid = true;
            
            // Clear previous errors
            document.querySelectorAll('.error-message').forEach(error => {
                error.style.display = 'none';
            });

            // Validate Full Name
            const fullName = document.getElementById('fullName').value.trim();
            if (fullName.length < 2) {
                document.getElementById('fullNameError').textContent = 'Full name must be at least 2 characters';
                document.getElementById('fullNameError').style.display = 'block';
                isValid = false;
            }

            // Validate Email
            const email = document.getElementById('email').value.trim();
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(email)) {
                document.getElementById('emailError').textContent = 'Please enter a valid email address';
                document.getElementById('emailError').style.display = 'block';
                isValid = false;
            }

            // Validate Specialization
            const specialization = document.getElementById('specialization').value;
            if (!specialization) {
                document.getElementById('specializationError').textContent = 'Please select your specialization';
                document.getElementById('specializationError').style.display = 'block';
                isValid = false;
            }

            // Validate License Number
            const licenseNumber = document.getElementById('licenseNumber').value.trim();
            if (licenseNumber.length < 5) {
                document.getElementById('licenseNumberError').textContent = 'Please enter a valid medical license number';
                document.getElementById('licenseNumberError').style.display = 'block';
                isValid = false;
            }

            // Validate Password
            const password = document.getElementById('password').value;
            if (password.length < 6) {
                document.getElementById('passwordError').textContent = 'Password must be at least 6 characters';
                document.getElementById('passwordError').style.display = 'block';
                isValid = false;
            }

            // Validate Confirm Password
            const confirmPassword = document.getElementById('confirmPassword').value;
            if (password !== confirmPassword) {
                document.getElementById('confirmPasswordError').textContent = 'Passwords do not match';
                document.getElementById('confirmPasswordError').style.display = 'block';
                isValid = false;
            }

            return isValid;
        }

        document.getElementById('doctorSignupForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (validateForm()) {
                // Show success message
                document.getElementById('successMessage').style.display = 'block';
                
                // Here you would typically send data to your backend
                const formData = {
                    fullName: document.getElementById('fullName').value,
                    email: document.getElementById('email').value,
                    specialization: document.getElementById('specialization').value,
                    licenseNumber: document.getElementById('licenseNumber').value,
                    password: document.getElementById('password').value,
                    userType: 'doctor'
                };
                
                console.log('Doctor signup data:', formData);
                
                // Simulate redirect after 2 seconds
                setTimeout(() => {
                    // window.location.href = 'doctor-login.html';
                    alert('Signup successful! You can now implement the redirect to login page.');
                }, 2000);
            }
        });

        // Real-time validation
        document.getElementById('confirmPassword').addEventListener('input', function() {
            const password = document.getElementById('password').value;
            const confirmPassword = this.value;
            const errorElement = document.getElementById('confirmPasswordError');
            
            if (confirmPassword && password !== confirmPassword) {
                errorElement.textContent = 'Passwords do not match';
                errorElement.style.display = 'block';
            } else {
                errorElement.style.display = 'none';
            }
        });
