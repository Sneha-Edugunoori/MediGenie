        // Auto-refresh page every 5 minutes to check status
        setTimeout(() => {
            window.location.reload();
        }, 300000);

        // Add some interactive feedback
        document.querySelector('.verification-icon').addEventListener('click', function() {
            this.style.animation = 'none';
            setTimeout(() => {
                this.style.animation = 'pulse 2s infinite';
            }, 10);
        });

        // Simulate notification check (you would replace with actual API call)
        function checkVerificationStatus() {
            // This would be your actual API endpoint
            console.log('Checking verification status...');
            // If verified, redirect to login or dashboard
            // if (response.status === 'verified') {
            //     window.location.href = '/doctor/login?verified=true';
            // }
        }

        // Check status every 2 minutes
        setInterval(checkVerificationStatus, 120000);
