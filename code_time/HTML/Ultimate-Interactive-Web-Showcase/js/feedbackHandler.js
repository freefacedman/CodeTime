    // feedbackHandler.js

    /* Feedback Data Management */
    // Currently storing feedback in localStorage
    // For backend integration, implement API calls here

    function getAllFeedback() {
        return JSON.parse(localStorage.getItem('allFeedback')) || [];
    }

    function clearFeedback() {
        localStorage.removeItem('allFeedback');
    }

    /* Example Usage */
    // const feedbacks = getAllFeedback();
    // console.log(feedbacks);
