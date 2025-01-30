let alarmTime = null;
let stopwatchInterval;
let stopwatchRunning = false;
let stopwatchTime = 0;
let timerInterval;
let timerRunning = false;
let timerTime = 0;
let clockInterval; // Declare the clockInterval globally

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
    clearInterval(clockInterval); // Clear the previous interval before changing time zone
    
    const now = new Date();
    const options = { timeZone: timezone };
    const timeString = now.toLocaleTimeString('en-US', options);
    document.getElementById('digital-clock').textContent = timeString;
    
    // Start a new interval after changing time zone
    clockInterval = setInterval(updateClock, 1000);
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

function snoozeAlarm() {
    if (confirm("Are you sure you want to snooze the alarm?")) {
        // If user confirms, snooze the alarm (for example, by adding 5 minutes)
        const snoozeTime = new Date(alarmTime.getTime() + 5 * 60000); // Snooze for 5 minutes
        alarmTime = snoozeTime;
        updateAlarmList(); // Update alarm list after snoozing
    }
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

function startStopwatch() {
    if (!stopwatchRunning) {
        stopwatchInterval = setInterval(updateStopwatch, 1000);
        stopwatchRunning = true;
        document.getElementById('start-stopwatch').textContent = 'Stop';
    } else {
        clearInterval(stopwatchInterval);
        stopwatchRunning = false;
        document.getElementById('start-stopwatch').textContent = 'Start';
    }
}

function updateStopwatch() {
    stopwatchTime++;
    const hours = Math.floor(stopwatchTime / 3600);
    const minutes = Math.floor((stopwatchTime % 3600) / 60);
    const seconds = stopwatchTime % 60;
    const stopwatchString = `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)}`;
    document.getElementById('stopwatch-display').textContent = stopwatchString;
}

function resetStopwatch() {
    clearInterval(stopwatchInterval);
    stopwatchTime = 0;
    stopwatchRunning = false;
    document.getElementById('stopwatch-display').textContent = '00:00:00';
    document.getElementById('start-stopwatch').textContent = 'Start';
}

function startTimer() {
    if (!timerRunning) {
        timerInterval = setInterval(updateTimer, 1000);
        timerRunning = true;
        document.getElementById('start-timer').textContent = 'Pause';
    } else {
        clearInterval(timerInterval);
        timerRunning = false;
        document.getElementById('start-timer').textContent = 'Resume';
    }
}

function updateTimer() {
    timerTime--;
    if (timerTime < 0) {
        clearInterval(timerInterval);
        timerRunning = false;
        alert("Timer completed!");
        document.getElementById('start-timer').textContent = 'Start';
    } else {
        const hours = Math.floor(timerTime / 3600);
        const minutes = Math.floor((timerTime % 3600) / 60);
        const seconds = timerTime % 60;
        const timerString = `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)}`;
        document.getElementById('timer-display').textContent = timerString;
    }
}

function resetTimer() {
    clearInterval(timerInterval);
    timerTime = 0;
    timerRunning = false;
    document.getElementById('timer-display').textContent = '00:00:00';
    document.getElementById('start-timer').textContent = 'Start';
}

// Update the clock initially and every second
updateClock();
clockInterval = setInterval(updateClock, 1000); // Assign the interval ID to clockInterval
