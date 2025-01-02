// contactForm.js

/* Contact Form with Real-Time Validation */
const contactForm = document.getElementById('contactForm');
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const messageInput = document.getElementById('message');

nameInput.addEventListener('input', validateName);
emailInput.addEventListener('input', validateEmail);
messageInput.addEventListener('input', validateMessage);

function validateName() {
    if (nameInput.value.trim() === '') {
        nameInput.style.borderColor = '#f44336';
    } else {
        nameInput.style.borderColor = '#4CAF50';
    }
}

function validateEmail() {
    const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    if (!emailRegex.test(emailInput.value.trim())) {
        emailInput.style.borderColor = '#f44336';
    } else {
        emailInput.style.borderColor = '#4CAF50';
    }
}

function validateMessage() {
    if (messageInput.value.trim().length < 10) {
        messageInput.style.borderColor = '#f44336';
    } else {
        messageInput.style.borderColor = '#4CAF50';
    }
}

contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const message = messageInput.value.trim();

    if (name === '' || email === '' || message === '') {
        showToast('Please fill in all fields!');
        return;
    }

    // Save to localStorage
    const contactData = { name, email, message };
    localStorage.setItem('contactData', JSON.stringify(contactData));

    showToast('Message Sent Successfully!');
    contactForm.reset();
});
