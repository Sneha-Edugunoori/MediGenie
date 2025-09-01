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

            // Validate Email (must be government email)
            const email = document.getElementById('email').value.trim();
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const govEmailPattern = /\.(gov|gov\.in|nic\.in)$/i;
            
            if (!emailPattern.test(email)) {
                document.getElementById('emailError').textContent = 'Please enter a valid email address';
                document.getElementById('emailError').style.display = 'block';
                isValid = false;
            } else if (!govEmailPattern.test(email)) {
                document.getElementById('emailError').textContent = 'Please use an official government email address';
                document.getElementById('emailError').style.display = 'block';
                isValid = false;
            }

            // Validate Password
            const password = document.getElementById('password').value;
            if (password.length < 8) {
                document.getElementById('passwordError').textContent = 'Password must be at least 8 characters for security';
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

        document.getElementById('governmentSignupForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (validateForm()) {
                // Show success message
                document.getElementById('successMessage').style.display = 'block';
                
                // Here you would typically send data to your backend
                const formData = {
                    email: document.getElementById('email').value,
                    password: document.getElementById('password').value,
                    userType: 'government'
                };
                
                console.log('Government signup data:', formData);
                
                // Simulate redirect after 3 seconds (longer for government verification)
                setTimeout(() => {
                    // window.location.href = 'government-login.html';
                    alert('Account created! Please check your email for verification instructions.');
                }, 3000);
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

        // Real-time email validation
        document.getElementById('email').addEventListener('blur', function() {
            const email = this.value.trim();
            const govEmailPattern = /\.(gov|gov\.in|nic\.in)$/i;
            const errorElement = document.getElementById('emailError');
            
            if (email && !govEmailPattern.test(email)) {
                errorElement.textContent = 'Please use an official government email address';
                errorElement.style.display = 'block';
            } else {
                errorElement.style.display = 'none';
            }
        });
 