// Navigation (Mobile menu toggle)
function toggleMenu() {
    const menu = document.getElementById('navbarMenu');
    menu.classList.toggle('active');
}

// Dropdown toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function(dropdown) {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');

        if (toggle && menu) {
            // Toggle dropdown on click
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                // Close all other dropdowns
                dropdowns.forEach(function(otherDropdown) {
                    if (otherDropdown !== dropdown) {
                        otherDropdown.classList.remove('active');
                    }
                });

                // Toggle current dropdown
                dropdown.classList.toggle('active');
            });
        }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            dropdowns.forEach(function(dropdown) {
                dropdown.classList.remove('active');
            });
        }
    });
});

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

document.addEventListener('DOMContentLoaded', function() {
    const randomizer = document.querySelector('[data-hero-randomizer]');
    if (randomizer) {
        const taglines = [
            'Lose it?<br>Find it here.',
            'One stop<br>for lost items.',
            'Lost things,<br>found solutions.',
            'A helping hand<br>for lost items.',
            'Trusted to<br>find your lost items.'
        ];
        const randomIndex = Math.floor(Math.random() * taglines.length);
        const taglineText = randomizer.querySelector('.tagline-text');
        if (taglineText) {
            taglineText.innerHTML = taglines[randomIndex];
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const sliderRoots = document.querySelectorAll('[data-lf-slider]');
    sliderRoots.forEach(function(sliderRoot) {
        const slides = Array.from(sliderRoot.querySelectorAll('[data-lf-slide]'));
        const prevBtn = sliderRoot.querySelector('[data-lf-slider-prev]');
        const nextBtn = sliderRoot.querySelector('[data-lf-slider-next]');
        const viewport = sliderRoot.querySelector('.lf-slider-viewport');

        if (!slides.length || !viewport) return;

        let index = 0;

        function setActive(nextIndex) {
            index = ((nextIndex % slides.length) + slides.length) % slides.length;
            const scrollLeft = slides[index].offsetLeft - viewport.offsetLeft;
            viewport.scrollLeft = scrollLeft;
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                e.preventDefault();
                setActive(index - 1);
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                e.preventDefault();
                setActive(index + 1);
            });
        }

        setActive(0);
    });
});
