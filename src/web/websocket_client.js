// websocket_client.js

// Dynamic WebSocket URL
const websocketUrl = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") 
    ? "ws://127.0.0.1:8000/ws/logs"
    : "wss://sentinel-dashboard-hnfl5snxn-sentinels-projects-51a4a159.vercel.app/ws/logs";

console.log(`🔗 Connecting to WebSocket: ${websocketUrl}`);

const socket = new WebSocket(websocketUrl);

// UI Elements
const logContainer = document.getElementById("log-container");
const pauseButton = document.getElementById("pause-logs");
const clearButton = document.getElementById("clear-logs");
const filterInput = document.getElementById("filter-logs");

let isPaused = false;

// WebSocket Event Listeners
socket.onopen = () => {
    console.log("✅ Connected to WebSocket Server");
    addLogEntry("✅ Connected to WebSocket Server", "success");
};

socket.onmessage = (event) => {
    if (!isPaused) {
        addLogEntry(event.data);
    }
};

socket.onerror = (error) => {
    console.error("❌ WebSocket Error:", error);
    addLogEntry(`❌ WebSocket Error: ${error}`, "error");
};

socket.onclose = () => {
    console.log("🔌 Disconnected from WebSocket Server");
    addLogEntry("🔌 Disconnected from WebSocket Server", "warning");
};

// Utility Functions
function addLogEntry(message, type = "default") {
    const logEntry = document.createElement("div");
    logEntry.className = `log-entry ${type}`;
    logEntry.innerText = `[${new Date().toLocaleTimeString()}] ${message}`;
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

console.log(`✅ WebSocket Client Initialized. Using URL: ${websocketUrl}`);
