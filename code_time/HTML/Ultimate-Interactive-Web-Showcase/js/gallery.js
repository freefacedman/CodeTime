// gallery.js

/* Gallery Functionality */
window.openLightbox = function(src, alt) {
    const modal = document.getElementById('lightbox-modal');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    lightboxImg.src = src;
    lightboxImg.alt = alt;
    lightboxCaption.textContent = alt;
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
    trapFocus(modal);
    modal.querySelector('button, [href], input, select, textarea').focus();
}

window.closeLightbox = function() {
    const modal = document.getElementById('lightbox-modal');
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
}
    // gallery.js

    /* Gallery Functionality */
    window.openLightbox = function(src, alt) {
        const modal = document.getElementById('lightbox-modal');
        const lightboxImg = document.getElementById('lightbox-img');
        const lightboxCaption = document.getElementById('lightbox-caption');
        lightboxImg.src = src;
        lightboxImg.alt = alt;
        lightboxCaption.textContent = alt;
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        trapFocus(modal);
        modal.querySelector('button, [href], input, select, textarea').focus();
    }

    window.closeLightbox = function() {
        const modal = document.getElementById('lightbox-modal');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    /* Trap Focus in Lightbox Modal */
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
