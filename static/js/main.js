// Navigation (Mobile menu toggle)
function toggleMenu() {
    const menu = document.getElementById('navbarMenu');
    menu.classList.toggle('active');
}

// Alerts displaying success, warning messages
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // Fade out animation
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';

            // Remove from DOM after fade out
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000); // 5 seconds
    });
});

// Home page welcome message
document.addEventListener('DOMContentLoaded', function() {
    const welcomeMsg = document.getElementById('welcome-message');
    if (welcomeMsg) {
        // Check if the URL has login=1 parameter (redirected from login)
        const urlParams = new URLSearchParams(window.location.search);
        const isLoginRedirect = urlParams.get('login') === '1';

        if (isLoginRedirect) {
            // Show the message
            welcomeMsg.style.display = 'block';

            // Auto-dismiss after 5 seconds
            setTimeout(function() {
                // Fade out animation
                welcomeMsg.style.transition = 'opacity 0.5s ease';
                welcomeMsg.style.opacity = '0';

                // Remove from DOM after fade out
                setTimeout(function() {
                    welcomeMsg.remove();
                }, 500);
            }, 5000); // 5 seconds
        }
    }
});

// Claims, dynamic form based on claim type
document.addEventListener('DOMContentLoaded', function() {
    const claimRadio = document.querySelector('input[value="claim"]');
    const inquiryRadio = document.querySelector('input[value="inquiry"]');
    const descriptionLabel = document.getElementById('description-label');
    const descriptionHelp = document.getElementById('description-help');
    const descriptionTextarea = document.querySelector('#id_description');
    const additionalProofSection = document.getElementById('additional-proof-section');

    function updateForm() {
        if (claimRadio && claimRadio.checked) {
            // Claim mode - show proof fields
            if (descriptionLabel) descriptionLabel.textContent = 'Item Description / Proof of Ownership';
            if (descriptionHelp) descriptionHelp.textContent = 'Describe the item in detail to prove ownership. Include color, brand, size, distinguishing features, where you lost it, etc.';
            if (descriptionTextarea) descriptionTextarea.placeholder = 'Describe the item in detail. Include color, brand, size, distinguishing features, where you lost it, etc.';
            if (additionalProofSection) additionalProofSection.style.display = 'block';
        } else if (inquiryRadio && inquiryRadio.checked) {
            // Inquiry mode - hide proof fields
            if (descriptionLabel) descriptionLabel.textContent = 'Your Question or Inquiry';
            if (descriptionHelp) descriptionHelp.textContent = 'Ask a question about this item or request more information';
            if (descriptionTextarea) descriptionTextarea.placeholder = 'e.g., "Does this water bottle have a dent on the side?" or "Can you provide more details about where exactly it was found?"';
            if (additionalProofSection) additionalProofSection.style.display = 'none';
        }
    }

    // Listen for changes
    if (claimRadio) claimRadio.addEventListener('change', updateForm);
    if (inquiryRadio) inquiryRadio.addEventListener('change', updateForm);

    // Set initial state
    updateForm();
});
