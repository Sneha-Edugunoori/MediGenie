        function goBack() {
            // You can customize this to go to your main page
            window.history.back();
        }

        function forgotPassword() {
            alert('Forgot password functionality - you can implement this to redirect to password reset page');
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
            if (!emailPattern.test(email)) {
                document.getElementById('emailError').textContent = 'Please enter a valid email address';
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

        document.getElementById('doctorLoginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (validateForm()) {
                // Show success message
                document.getElementById('successMessage').style.display = 'block';
                
                // Here you would typically send data to your backend for authentication
                const formData = {
                    email: document.getElementById('email').value,
                    password: document.getElementById('password').value,
                    userType: 'doctor'
                };
                
                console.log('Doctor login data:', formData);
                
                // Simulate redirect after 2 seconds
                setTimeout(() => {
                    // window.location.href = 'doctor-dashboard.html';
                    alert('Login successful! You can now implement the redirect to doctor dashboard.');
                }, 2000);
            }
        });
  