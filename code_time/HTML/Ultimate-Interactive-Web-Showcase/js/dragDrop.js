    // dragDrop.js

    /* Drag and Drop Functionality with Reset */
    const draggables = document.querySelectorAll('.draggable');
    const dropzone = document.getElementById('dropzone');
    const benefitsInfo = document.getElementById('benefits-info');

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', dragStart);
        draggable.addEventListener('dragend', dragEnd);
    });

    dropzone.addEventListener('dragover', dragOver);
    dropzone.addEventListener('dragenter', dragEnter);
    dropzone.addEventListener('dragleave', dragLeave);
    dropzone.addEventListener('drop', drop);

    function dragStart(e) {
        e.dataTransfer.setData('text/plain', e.target.id);
        setTimeout(() => {
            e.target.classList.add('hide');
        }, 0);
    }

    function dragEnd(e) {
        e.target.classList.remove('hide');
    }

    function dragOver(e) {
        e.preventDefault();
    }

    function dragEnter(e) {
        e.preventDefault();
        dropzone.classList.add('hovered');
    }

    function dragLeave(e) {
        dropzone.classList.remove('hovered');
    }

    function drop(e) {
        e.preventDefault();
        dropzone.classList.remove('hovered');
        const id = e.dataTransfer.getData('text/plain');
        const draggable = document.getElementById(id);
        dropzone.innerHTML = '';
        dropzone.appendChild(draggable);
        draggable.style.cursor = 'default';
        showToast(`${draggable.textContent} dropped successfully!`);
        displayBenefits(draggable.dataset.type);
    }

    window.resetDropzone = function() {
        dropzone.innerHTML = '<p>Drop here</p>';
        benefitsInfo.innerHTML = '';
        benefitsInfo.classList.remove('active');
        showToast('Dropzone has been reset.');
    }

    /* Medical Benefits Data */
    const medicalBenefits = {
        reishi: {
            title: 'Medical Benefits of Reishi Mushroom',
            benefits: [
                'Boosts the immune system',
                'Reduces stress and fatigue',
                'Promotes better sleep',
                'May lower blood pressure',
                'Supports liver health'
            ]
        },
        'lions-mane': {
            title: 'Medical Benefits of Lion\'s Mane Mushroom',
            benefits: [
                'Enhances cognitive function',
                'Promotes nerve growth',
                'May reduce symptoms of anxiety and depression',
                'Supports digestive health',
                'Boosts immune system'
            ]
        },
        creatine: {
            title: 'Medical Benefits of Creatine',
            benefits: [
                'Improves muscle strength and power',
                'Supports muscle growth',
                'Enhances athletic performance',
                'Aids in recovery after exercise',
                'May support brain health'
            ]
        }
    }

    /* Function to Display Benefits */
    function displayBenefits(type) {
        if (medicalBenefits[type]) {
            const data = medicalBenefits[type];
            benefitsInfo.innerHTML = `
                <h3>${data.title}</h3>
                <ul>
                    ${data.benefits.map(benefit => `<li>${benefit}</li>`).join('')}
                </ul>
            `;
            benefitsInfo.classList.add('active');
        } else {
            benefitsInfo.innerHTML = '';
            benefitsInfo.classList.remove('active');
        }
    }
