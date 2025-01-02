// JavaScript for Digital Clock with Alarms

let alarmTime = null;

function updateClock() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();
    const meridiem = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12 || 12; // Convert to 12-hour format
    const timeString = `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)} ${meridiem}`;
    document.getElementById('digital-clock').textContent = timeString;

    // Check if alarmTime is set and matches the current time
    if (alarmTime && now.getHours() === alarmTime.getHours() && now.getMinutes() === alarmTime.getMinutes()) {
        playAlarmSound();
        alert('Alarm!');
        const selectedAnimation = document.getElementById('alarm-animation').value;
        document.getElementById('clock').classList.add(selectedAnimation); // Add selected animation class
        // Optionally, you can play a sound, show a message, or perform any other action here
        alarmTime = null; // Reset alarmTime after it's triggered
        updateAlarmList(); // Update alarm list after alarm triggers
    }
}

function padZero(num) {
    return num < 10 ? `0${num}` : num;
}

function changeTimeZone(timezone) {
    // You can implement timezone handling if necessary
    // For a digital clock, it typically displays local time
}

function setAlarm() {
    const alarmInput = document.getElementById('alarm-time');
    const alarmTimeString = alarmInput.value;
    const [alarmHour, alarmMinute] = alarmTimeString.split(':').map(Number);
    alarmTime = new Date();
    alarmTime.setHours(alarmHour);
    alarmTime.setMinutes(alarmMinute);
    alarmTime.setSeconds(0);
    updateAlarmList(); // Update alarm list after setting a new alarm
}

function updateAlarmList() {
    const alarmList = document.getElementById('alarm-list');
    const alarms = alarmList.getElementsByTagName('li');
    // Clear existing alarms
    for (let i = alarms.length - 1; i >= 0; i--) {
        alarms[i].remove();
    }
    // Add current alarms
    if (alarmTime) {
        const alarmItem = document.createElement('li');
        alarmItem.textContent = `${padZero(alarmTime.getHours())}:${padZero(alarmTime.getMinutes())}`;
        const removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.className = 'remove-button'; // Add remove button class
        removeButton.onclick = function() {
            alarmTime = null;
            updateAlarmList();
        };
        alarmItem.appendChild(removeButton);
        alarmList.appendChild(alarmItem);
    }
}

function playAlarmSound() {
    const soundSelect = document.getElementById('alarm-sound');
    const selectedSound = soundSelect.value;
    const audio = new Audio(selectedSound);
    audio.play();
}

// Update the clock initially and every second
updateClock();
setInterval(updateClock, 1000);
