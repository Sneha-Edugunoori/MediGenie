        function goBack() {
            // You can customize this to go to your main page
            window.history.back();
        }

        function forgotPassword() {
            alert('For password reset, please contact your IT administrator or use the government portal help desk.');
        }

        function validateForm() {
            let isValid = true;
            
            // Clear previous errors
            document.querySelectorAll('.error-message').forEach(error => {
                error.style.display = 'none';
            });

            // Validate Email
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
            if (password.length < 1) {
                document.getElementById('passwordError').textContent = 'Password is required';
                document.getElementById('passwordError').style.display = 'block';
                isValid = false;
            }

            return isValid;
        }

        document.getElementById('governmentLoginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (validateForm()) {
                // Show success message
                document.getElementById('successMessage').style.display = 'block';
                
                // Here you would typically send data to your backend for authentication
                const formData = {
                    email: document.getElementById('email').value,
                    password: document.getElementById('password').value,
                    userType: 'government'
                };
                
                console.log('Government login data:', formData);
                
                // Simulate redirect after 2 seconds
                setTimeout(() => {
                    // window.location.href = 'government-dashboard.html';
                    alert('Login successful! You can now implement the redirect to government dashboard.');
                }, 2000);
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
