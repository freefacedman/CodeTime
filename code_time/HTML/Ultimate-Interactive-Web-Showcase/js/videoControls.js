// videoControls.js

/* Video Controls */
const myVideo = document.getElementById('myVideo');

window.playVideo = function() {
    myVideo.play();
}

window.pauseVideo = function() {
    myVideo.pause();
}

window.stopVideo = function() {
    myVideo.pause();
    myVideo.currentTime = 0;
}
