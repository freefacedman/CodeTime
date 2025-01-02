// quizGame.js

/* Quiz Game Enhancements */
const quizData = [
    {
        question: 'What is the capital of France?',
        options: ['Berlin', 'London', 'Paris', 'Madrid'],
        answer: 'Paris'
    },
    {
        question: 'Which planet is known as the Red Planet?',
        options: ['Earth', 'Mars', 'Jupiter', 'Venus'],
        answer: 'Mars'
    },
    {
        question: 'Who wrote \'Romeo and Juliet\'?',
        options: ['Mark Twain', 'William Shakespeare', 'Charles Dickens', 'Jane Austen'],
        answer: 'William Shakespeare'
    }
];

let currentQuiz = 0;
let score = 0;

function updateProgressBar() {
    const progressBar = document.getElementById('quizProgressBar');
    const progressPercentage = ((currentQuiz) / quizData.length) * 100;
    progressBar.style.width = ${progressPercentage}%;
}

function loadQuiz() {
    const savedProgress = JSON.parse(localStorage.getItem('quizProgress'));
    if (savedProgress) {
        currentQuiz = savedProgress.currentQuiz;
        score = savedProgress.score;
    }

    const quizQuestion = document.getElementById('quiz-question');
    const quizOptions = document.getElementById('quiz-options');
    const quizResult = document.getElementById('quiz-result');
    updateProgressBar();

    if (currentQuiz < quizData.length) {
        const currentData = quizData[currentQuiz];
        quizQuestion.textContent = currentData.question;
        quizOptions.innerHTML = '';
        currentData.options.forEach(option => {
            const button = document.createElement('button');
            button.textContent = option;
            button.onclick = () => selectAnswer(option);
            quizOptions.appendChild(button);
        });
        quizResult.textContent = '';
    } else {
        quizQuestion.textContent = You scored  out of ;
        quizOptions.innerHTML = '';
        const restartBtn = document.createElement('button');
        restartBtn.textContent = 'Restart Quiz';
        restartBtn.onclick = restartQuiz;
        quizOptions.appendChild(restartBtn);
    }
}

function selectAnswer(selected) {
    const correct = quizData[currentQuiz].answer;
    if (selected === correct) {
        score++;
        showToast('Correct Answer!');
    } else {
        showToast(Wrong! Correct Answer: );
    }
    currentQuiz++;
    localStorage.setItem('quizProgress', JSON.stringify({ currentQuiz, score }));
    loadQuiz();
}

function restartQuiz() {
    currentQuiz = 0;
    score = 0;
    localStorage.removeItem('quizProgress');
    loadQuiz();
}

/* Initialize Quiz on DOM Load */
loadQuiz();
