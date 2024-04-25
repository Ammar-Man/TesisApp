

//   <h1>Timer</h1>
//   <p>Counter ID: <span id="counterId">1</span></p>
//   <p>Time: <span id="timer">00:00:00</span></p>
//   <button id="startBtn">Start</button>
//   <button id="stopBtn">Stop</button>




let timerInterval;
let startTime;
let counterId=1;

// Initialize timerInterval to zero
timerInterval = 0;
// const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const timerDisplay = document.getElementById('timer');
// const counterIdDisplay = document.getElementById('counterId');

document.addEventListener("DOMContentLoaded", function() {
  // Get the last index ID from localStorage
  const data = localStorage.getItem("timer_data.csv");
  counterId = getLastIndex(data) + 1 || 1; // If localStorage is empty, start from 1
  console.log("counterId: "+counterId);
//   counterIdDisplay.textContent = counterId;
});

// startBtn.addEventListener('click', startTimer);
stopBtn.addEventListener('click', stopTimer);

startTimer();

function startTimer() {
  console.log("timerInterval: "+timerInterval);
  startTime = Date.now() - (counterId === 1 ? 0 : timerInterval);
  console.log("startTime: "+startTime);
  timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
  clearInterval(timerInterval);
  const elapsedTime = Date.now() - startTime;
  // timerDisplay.textContent = formatTime(elapsedTime);
  console.log("stopTimer: ",console_Timer);

  saveToCSV(counterId, new Date().toLocaleString());
  counterId++;
//   counterIdDisplay.textContent = counterId;
}
let console_Timer = 0;
function updateTimer() {
  const elapsedTime = Date.now() - startTime;
  console_Timer = formatTime(elapsedTime)
  // timerDisplay.textContent = formatTime(elapsedTime);
  console.log("timer: ",console_Timer);
}

function formatTime(milliseconds) {
  const hours = Math.floor(milliseconds / 3600000);
  const minutes = Math.floor((milliseconds % 3600000) / 60000);
  const seconds = Math.floor((milliseconds % 60000) / 1000);
  return `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)}`;
}

function padZero(num) {
  return (num < 10 ? '0' : '') + num;
}

function saveToCSV(id, date) {
  const time = console_Timer; // Get the current timer value
  // const time = timerDisplay.textContent; // Get the current timer value
  const csvRow = `${id},${time},${date}\n`;
  const csvContent = csvRow;
  const fileName = 'timer_data.csv';
  
  if (checkIfFileExists(fileName)) {
    appendToCSV(fileName, csvContent);
  } else {
    alert("I can't find your CSV file. Need help?");
    createNewCSV(fileName, csvContent);
  }
}

function getLastIndex(data) {
  let lastIndex = 0;
  if (data) {
    const lines = data.split('\n');
    if (lines.length > 0) {
      const lastLine = lines[lines.length - 2]; // -2 to avoid empty line at the end
      const parts = lastLine.split(',');
      if (parts.length > 0) {
        lastIndex = parseInt(parts[0]);
      }
    }
  }
  return lastIndex;
}

function checkIfFileExists(fileName) {
  return localStorage.getItem(fileName) !== null;
}

function appendToCSV(fileName, data) {
  const existingData = localStorage.getItem(fileName);
  const newData = existingData + data;
  localStorage.setItem(fileName, newData);
}

function createNewCSV(fileName, data) {
  localStorage.setItem(fileName, data);
}




