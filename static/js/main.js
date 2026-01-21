// MOBILE MENU TOGGLE (with ARIA support)
function toggleMenu() {
    const menu = document.getElementById('navbarMenu');
    const toggle = document.querySelector('.navbar-toggle');
    const isExpanded = menu.classList.contains('active');
    
    menu.classList.toggle('active');

    if (toggle) {
        toggle.setAttribute('aria-expanded', String(!isExpanded));
    }
}



// DROPDOWN TOGGLE (with keyboard support)
document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function(dropdown) {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');

        if (toggle && menu) {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                toggleDropdownState();
            });

            toggle.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleDropdownState();
                }
                if (e.key === 'Escape') {
                    closeDropdown();
                }
            });

            function toggleDropdownState() {
                const isOpen = dropdown.classList.contains('active');

                // Close other dropdowns
                dropdowns.forEach(function(otherDropdown) {
                    if (otherDropdown !== dropdown) {
                        otherDropdown.classList.remove('active');
                        const otherToggle = otherDropdown.querySelector('.dropdown-toggle');
                        if (otherToggle) {
                            otherToggle.setAttribute('aria-expanded', 'false');
                        }
                    }
                });

                dropdown.classList.toggle('active');
                toggle.setAttribute('aria-expanded', String(!isOpen));

                if (!isOpen) {
                    setTimeout(function() {
                        const firstLink = menu.querySelector('a');
                        if (firstLink) firstLink.focus();
                    }, 0);
                }
            }

            function closeDropdown() {
                dropdown.classList.remove('active');
                toggle.setAttribute('aria-expanded', 'false');
                toggle.focus();
            }
        }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            dropdowns.forEach(function(dropdown) {
                dropdown.classList.remove('active');
                const toggle = dropdown.querySelector('.dropdown-toggle');
                if (toggle) {
                    toggle.setAttribute('aria-expanded', 'false');
                }
            });
        }
    });
});



// ALERT AUTO-DISMISS
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        if (alert.classList.contains('static-alert')) return;

        setTimeout(function() {
            alert.setAttribute('aria-live', 'off');
            
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';

            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
});



// HOME PAGE WELCOME MESSAGE
document.addEventListener('DOMContentLoaded', function() {
    const welcomeMsg = document.getElementById('welcome-message');
    if (welcomeMsg) {
        const urlParams = new URLSearchParams(window.location.search);
        const isLoginRedirect = urlParams.get('login') === '1';

        if (isLoginRedirect) {
            welcomeMsg.style.display = 'block';
            welcomeMsg.setAttribute('role', 'status');
            welcomeMsg.setAttribute('aria-live', 'polite');

            setTimeout(function() {
                welcomeMsg.setAttribute('aria-live', 'off');
                welcomeMsg.style.transition = 'opacity 0.5s ease';
                welcomeMsg.style.opacity = '0';

                setTimeout(function() {
                    welcomeMsg.remove();
                }, 500);
            }, 5000);
        }
    }
});



// CLAIMS FORM LOGIC
document.addEventListener('DOMContentLoaded', function() {
    const claimRadio = document.querySelector('input[value="claim"]');
    const inquiryRadio = document.querySelector('input[value="inquiry"]');
    const descriptionLabel = document.getElementById('description-label');
    const descriptionHelp = document.getElementById('description-help');
    const descriptionTextarea = document.querySelector('#id_description');
    const additionalProofSection = document.getElementById('additional-proof-section');

    function updateForm() {
        if (claimRadio && claimRadio.checked) {
            if (descriptionLabel) descriptionLabel.textContent = 'Item Description / Proof of Ownership';
            if (descriptionHelp) descriptionHelp.textContent = 'Describe the item in detail to prove ownership. Include color, brand, size, distinguishing features, where you lost it, etc.';
            if (descriptionTextarea) {
                descriptionTextarea.placeholder = 'Describe the item in detail. Include color, brand, size, distinguishing features, where you lost it, etc.';
                descriptionTextarea.setAttribute('aria-describedby', 'description-help');
            }
            if (additionalProofSection) {
                additionalProofSection.style.display = 'block';
                const proofTextarea = additionalProofSection.querySelector('textarea');
                if (proofTextarea) proofTextarea.removeAttribute('aria-hidden');
            }
        }
        else if (inquiryRadio && inquiryRadio.checked) {
            if (descriptionLabel) descriptionLabel.textContent = 'Your Question or Inquiry';
            if (descriptionHelp) descriptionHelp.textContent = 'Ask a question about this item or request more information';
            if (descriptionTextarea) {
                descriptionTextarea.placeholder = 'e.g., "Does this water bottle have a dent on the side?" or "Can you provide more details about where exactly it was found?"';
                descriptionTextarea.setAttribute('aria-describedby', 'description-help');
            }
            if (additionalProofSection) {
                additionalProofSection.style.display = 'none';
                const proofTextarea = additionalProofSection.querySelector('textarea');
                if (proofTextarea) proofTextarea.setAttribute('aria-hidden', 'true');
            }
        }
    }

    if (claimRadio) claimRadio.addEventListener('change', updateForm);
    if (inquiryRadio) inquiryRadio.addEventListener('change', updateForm);

    updateForm();
});



// HERO TAGLINE RANDOMIZER
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
            taglineText.setAttribute('role', 'status');
            taglineText.setAttribute('aria-live', 'polite');
        }
    }
});



// IMAGE SLIDER (with keyboard support)
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

            slides.forEach(function(slide, i) {
                slide.setAttribute('aria-hidden', i === index ? 'false' : 'true');
                slide.setAttribute('tabindex', i === index ? '0' : '-1');
            });

            if (prevBtn) {
                prevBtn.setAttribute('aria-label', 'Previous slide, ' + (index + 1) + ' of ' + slides.length);
            }
            if (nextBtn) {
                nextBtn.setAttribute('aria-label', 'Next slide, ' + (index + 1) + ' of ' + slides.length);
            }
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                e.preventDefault();
                setActive(index - 1);
            });
            prevBtn.setAttribute('type', 'button');
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                e.preventDefault();
                setActive(index + 1);
            });
            nextBtn.setAttribute('type', 'button');
        }

        viewport.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                setActive(index - 1);
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                setActive(index + 1);
            }
        });

        setActive(0);

        viewport.setAttribute('role', 'region');
        viewport.setAttribute('aria-label', 'Image carousel');
        viewport.setAttribute('tabindex', '0');
    });
});



// FORM VALIDATION ENHANCEMENTS
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        const requiredInputs = form.querySelectorAll('[required]');
        
        requiredInputs.forEach(function(input) {
            input.setAttribute('aria-required', 'true');
            
            input.addEventListener('invalid', function(e) {
                e.preventDefault();
                input.setAttribute('aria-invalid', 'true');
                input.classList.add('is-invalid');

                let errorMsg = input.parentElement.querySelector('.error-message');
                if (!errorMsg) {
                    errorMsg = document.createElement('span');
                    errorMsg.className = 'error-message';
                    errorMsg.setAttribute('role', 'alert');
                    input.parentElement.appendChild(errorMsg);
                }

                errorMsg.textContent = input.validationMessage;

                const errorId = input.id + '-error';
                errorMsg.id = errorId;
                input.setAttribute('aria-describedby', errorId);
            });
            
            input.addEventListener('input', function() {
                if (input.checkValidity()) {
                    input.setAttribute('aria-invalid', 'false');
                    input.classList.remove('is-invalid');
                    
                    const errorMsg = input.parentElement.querySelector('.error-message');
                    if (errorMsg) errorMsg.remove();
                }
            });
        });
    });
});



// TOOLTIP SYSTEM
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.lf-hover-tooltip')) return;

    const tooltip = document.createElement('div');
    tooltip.className = 'lf-hover-tooltip';

    const titleEl = document.createElement('div');
    titleEl.className = 'lf-hover-tooltip-title';

    const metaEl = document.createElement('div');
    metaEl.className = 'lf-hover-tooltip-meta';

    tooltip.appendChild(titleEl);
    tooltip.appendChild(metaEl);
    document.body.appendChild(tooltip);

    let activeTarget = null;

    function setTooltipContent(target) {
        const title = target.dataset.title || '';
        const dateFound = target.dataset.dateFound || '';
        const category = target.dataset.category || '';
        const location = target.dataset.location || '';

        titleEl.textContent = title;

        const parts = [];
        if (dateFound) parts.push('Found: ' + dateFound);
        if (category) parts.push('Category: ' + category);
        if (location) parts.push('Location: ' + location);
        metaEl.textContent = parts.join(' · ');
    }

    function setTooltipPosition(clientX, clientY) {
        const margin = 12;
        const offsetY = 16;

        tooltip.style.left = clientX + 'px';
        tooltip.style.top = (clientY + offsetY) + 'px';

        const rect = tooltip.getBoundingClientRect();

        let nextLeft = clientX;
        const minLeft = rect.width / 2 + margin;
        const maxLeft = window.innerWidth - rect.width / 2 - margin;

        if (nextLeft < minLeft) nextLeft = minLeft;
        if (nextLeft > maxLeft) nextLeft = maxLeft;
        tooltip.style.left = nextLeft + 'px';

        if (rect.bottom > window.innerHeight - margin) {
            tooltip.style.top = (clientX - rect.height - offsetY) + 'px';
        }
    }

    document.body.addEventListener('mouseover', function(e) {
        const target = e.target.closest('[data-lf-tooltip]');
        if (target) {
            activeTarget = target;
            setTooltipContent(target);
            tooltip.classList.add('is-visible');
            setTooltipPosition(e.clientX, e.clientY);
        }
    });

    document.body.addEventListener('mousemove', function(e) {
        if (activeTarget) {
            setTooltipPosition(e.clientX, e.clientY);
        }
    });

    document.body.addEventListener('mouseout', function(e) {
        const target = e.target.closest('[data-lf-tooltip]');
        if (target && target === activeTarget) {
            if (!target.contains(e.relatedTarget)) {
                activeTarget = null;
                tooltip.classList.remove('is-visible');
            }
        }
    });

    window.addEventListener('scroll', function() {
        if (!activeTarget) return;
        tooltip.classList.remove('is-visible');
        activeTarget = null;
    }, { passive: true });
});



// FOCUS VISIBLE POLYFILL
document.addEventListener('DOMContentLoaded', function() {
    let hadKeyboardEvent = false;

    document.addEventListener('keydown', function() {
        hadKeyboardEvent = true;
        document.body.classList.add('using-keyboard');
    });

    document.addEventListener('mousedown', function() {
        if (hadKeyboardEvent) {
            hadKeyboardEvent = false;
            document.body.classList.remove('using-keyboard');
        }
    });

    document.addEventListener('focusin', function(e) {
        if (hadKeyboardEvent) {
            e.target.classList.add('focus-visible');
        }
    });

    document.addEventListener('focusout', function(e) {
        e.target.classList.remove('focus-visible');
    });
});
