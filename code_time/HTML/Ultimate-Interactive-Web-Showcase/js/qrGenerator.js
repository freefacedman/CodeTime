// qrGenerator.js

window.generateQRCode = function() {
    const linkInput = document.getElementById('link');
    const link = linkInput.value.trim();
    const color = document.getElementById('qr-color').value;
    const size = parseInt(document.getElementById('qr-size').value);
    const errorCorrection = document.getElementById('qr-error').value;
    const qrContainer = document.getElementById('qr-code');
    const qrModalCanvas = document.getElementById('qr-code-modal');
    qrContainer.innerHTML = '';
    qrModalCanvas.innerHTML = '';

    // Real-time validation
    if (!isValidURL(link)) {
        showToast('Please enter a valid URL!');
        linkInput.focus();
        return;
    }

    // Generate QR Code in Canvas
    QRCode.toCanvas(qrContainer, link, { 
        width: size,
        color: {
            dark: color,  // QR code color
            light: '#ffffff' // Background color
        },
        errorCorrectionLevel: errorCorrection
    }, function (error, canvas) {
        if (error) {
            console.error(error);
            showToast('Failed to generate QR code.');
        } else {
            // Clone the canvas for the modal
            const clonedCanvas = canvas.cloneNode(true);
            clonedCanvas.width = size * 2; // Increase size for modal
            clonedCanvas.height = size * 2;
            QRCode.toCanvas(clonedCanvas, link, { 
                width: size * 2,
                color: {
                    dark: color, 
                    light: '#ffffff'
                },
                errorCorrectionLevel: errorCorrection
            }, function (err) {
                if (err) {
                    console.error(err);
                    showToast('Failed to generate QR code for modal.');
                } else {
                    qrModalCanvas.appendChild(clonedCanvas);
                }
            });
        }
    });

    // Add click event to open modal
    qrContainer.onclick = function() {
        openModal();
    }
}

// URL Validation Function
function isValidURL(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;  
    }
}
