// modals.js

/* Modal Functionality */
window.openModal = function() {
    const modal = document.getElementById('qr-modal');
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
    trapFocus(modal);
    modal.querySelector('button, [href], input, select, textarea').focus();
}

window.closeModal = function() {
    const modal = document.getElementById('qr-modal');
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
}

window.openInfoModal = function() {
    const modal = document.getElementById('info-modal');
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
    trapFocus(modal);
    modal.querySelector('button, [href], input, select, textarea').focus();
}

window.closeInfoModal = function() {
    const modal = document.getElementById('info-modal');
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
}

/* Global Click Event for Closing Modals */
window.onclick = function(event) {
    const qrModal = document.getElementById('qr-modal');
    const lightboxModal = document.getElementById('lightbox-modal');
    const infoModal = document.getElementById('info-modal');
    const feedbackModal = document.getElementById('feedback-modal');
    if (event.target == qrModal) {
        closeModal();
    }
    if (event.target == lightboxModal) {
        closeLightbox();
    }
    if (event.target == infoModal) {
        closeInfoModal();
    }
    if (event.target == feedbackModal) {
        closeFeedbackModal();
    }
}
    // Enhanced modals.js
    
    /* Modal Functionality */
    window.openModal = function() {
        const modal = document.getElementById('qr-modal');
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        trapFocus(modal);
        modal.querySelector('button, [href], input, select, textarea').focus();
    }
    
    window.closeModal = function() {
        const modal = document.getElementById('qr-modal');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }
    
    window.openInfoModal = function() {
        const modal = document.getElementById('info-modal');
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        trapFocus(modal);
        modal.querySelector('button, [href], input, select, textarea').focus();
    }
    
    window.closeInfoModal = function() {
        const modal = document.getElementById('info-modal');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }
    
    window.openFeedbackModal = function() {
        const modal = document.getElementById('feedback-modal');
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        trapFocus(modal);
        modal.querySelector('button, [href], input, select, textarea').focus();
    }
    
    window.closeFeedbackModal = function() {
        const modal = document.getElementById('feedback-modal');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }
    
    /* Global Click Event for Closing Modals */
    window.onclick = function(event) {
        const qrModal = document.getElementById('qr-modal');
        const lightboxModal = document.getElementById('lightbox-modal');
        const infoModal = document.getElementById('info-modal');
        const feedbackModal = document.getElementById('feedback-modal');
        if (event.target -eq qrModal) {
            closeModal();
        }
        if (event.target -eq lightboxModal) {
            closeLightbox();
        }
        if (event.target -eq infoModal) {
            closeInfoModal();
        }
        if (event.target -eq feedbackModal) {
            closeFeedbackModal();
        }
    }
    
    /* Enhanced Accessibility: Trap Focus in Modals */
    function trapFocus(modal) {
        const focusableElements = modal.querySelectorAll('a[href], button, textarea, input, select');
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
    
        modal.addEventListener('keydown', function(e) {
            const isTabPressed = (e.key === 'Tab' || e.keyCode -eq 9);
    
            if (-not ) { return }
    
            if (.shiftKey) { # Shift + Tab
                if (.activeElement -eq ) {
                    .focus()
                    .preventDefault()
                }
            } else { # Tab
                if (.activeElement -eq ) {
                    .focus()
                    .preventDefault()
                }
            }
        })
    }
    // modals.js

    /* Modal Functionality */
    window.openModal = function() {
        const modal = document.getElementById('qr-modal');
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        trapFocus(modal);
        modal.querySelector('button, [href], input, select, textarea').focus();
    }

    window.closeModal = function() {
        const modal = document.getElementById('qr-modal');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    window.openInfoModal = function() {
        const modal = document.getElementById('info-modal');
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        trapFocus(modal);
        modal.querySelector('button, [href], input, select, textarea').focus();
    }

    window.closeInfoModal = function() {
        const modal = document.getElementById('info-modal');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    window.openFeedbackModal = function() {
        const modal = document.getElementById('feedback-modal');
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        trapFocus(modal);
        modal.querySelector('button, [href], input, select, textarea').focus();
    }

    window.closeFeedbackModal = function() {
        const modal = document.getElementById('feedback-modal');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    /* Global Click Event for Closing Modals */
    window.onclick = function(event) {
        const qrModal = document.getElementById('qr-modal');
        const lightboxModal = document.getElementById('lightbox-modal');
        const infoModal = document.getElementById('info-modal');
        const feedbackModal = document.getElementById('feedback-modal');
        if (event.target === qrModal) {
            closeModal();
        }
        if (event.target === lightboxModal) {
            closeLightbox();
        }
        if (event.target === infoModal) {
            closeInfoModal();
        }
        if (event.target === feedbackModal) {
            closeFeedbackModal();
        }
    }

    /* Enhanced Accessibility: Trap Focus in Modals */
    function trapFocus(modal) {
        const focusableElements = modal.querySelectorAll('a[href], button, textarea, input, select');
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        modal.addEventListener('keydown', function(e) {
            const isTabPressed = (e.key === 'Tab' || e.keyCode -eq 9);

            if (!isTabPressed) { return }

            if (e.shiftKey) { # Shift + Tab
                if (document.activeElement -eq firstElement) {
                    lastElement.focus()
                    e.preventDefault()
                }
            } else { # Tab
                if (document.activeElement -eq lastElement) {
                    firstElement.focus()
                    e.preventDefault()
                }
            }
        })
    }
