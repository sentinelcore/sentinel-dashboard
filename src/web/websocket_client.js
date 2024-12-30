// Establish WebSocket Connection
const socket = new WebSocket("ws://127.0.0.1:8000/ws/logs");

// Get UI Elements
const logContainer = document.getElementById("log-container");
const pauseButton = document.getElementById("pause-logs");
const clearButton = document.getElementById("clear-logs");
const filterInput = document.getElementById("filter-logs");

let isPaused = false;

// WebSocket Event Listeners
socket.onopen = () => {
    console.log("✅ Connected to WebSocket Server");
    addLogEntry("✅ Connected to WebSocket Server");
};

socket.onmessage = (event) => {
    if (!isPaused) {
        addLogEntry(event.data);
    }
};

socket.onerror = (error) => {
    console.error("❌ WebSocket Error:", error);
    addLogEntry(`❌ WebSocket Error: ${error}`);
};

socket.onclose = () => {
    console.log("🔌 Disconnected from WebSocket Server");
    addLogEntry("🔌 Disconnected from WebSocket Server");
};

// Utility Functions
function addLogEntry(message) {
    const logEntry = document.createElement("div");
    logEntry.className = "log-entry";
    logEntry.innerText = `[${new Date().toLocaleTimeString()}] ${message}`;

    if (message.includes("✅")) {
        logEntry.style.color = "green";
    } else if (message.includes("❌") || message.includes("⚠️")) {
        logEntry.style.color = "red";
    } else {
        logEntry.style.color = "black";
    }

    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

function clearLogs() {
    logContainer.innerHTML = "";
}

function togglePauseLogs() {
    isPaused = !isPaused;
    pauseButton.innerText = isPaused ? "Resume Logs" : "Pause Logs";
}

function filterLogs() {
    const filterText = filterInput.value.toLowerCase();
    const entries = document.querySelectorAll(".log-entry");
    entries.forEach(entry => {
        if (entry.innerText.toLowerCase().includes(filterText)) {
            entry.style.display = "block";
        } else {
            entry.style.display = "none";
        }
    });
}

// Button Event Listeners
pauseButton.addEventListener("click", togglePauseLogs);
clearButton.addEventListener("click", clearLogs);
filterInput.addEventListener("input", filterLogs);

console.log("✅ WebSocket Client Initialized");
