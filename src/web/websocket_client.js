// =========================
// 📡 WebSocket for Logs
// =========================

// UI Elements for Logs
const logContainer = document.getElementById("log-container");
const pauseButton = document.getElementById("pause-logs");
const clearButton = document.getElementById("clear-logs");
const filterInput = document.getElementById("filter-logs");

let isPaused = false;
let filterText = "";

// Initialize WebSocket for Logs
const logSocket = new WebSocket("ws://127.0.0.1:8000/ws/logs");

// WebSocket Event Listeners for Logs
logSocket.onopen = () => {
    console.log("✅ Connected to Logs WebSocket");
    addLogEntry("✅ Connected to Logs WebSocket", "success");
};

logSocket.onmessage = (event) => {
    if (!isPaused) {
        const data = JSON.parse(event.data);
        if (data.type === "log") {
            addLogEntry(data.message, "default");
        }
    }
};

logSocket.onerror = (error) => {
    console.error("❌ Logs WebSocket Error:", error);
    addLogEntry(`❌ Logs WebSocket Error: ${error}`, "error");
};

logSocket.onclose = () => {
    console.warn("🔌 Logs WebSocket Disconnected");
    addLogEntry("🔌 Logs WebSocket Disconnected", "warning");
};

// Utility Functions for Logs
function addLogEntry(message, type = "default") {
    const logEntry = document.createElement("div");
    logEntry.className = `log-entry ${type}`;
    logEntry.innerText = `[${new Date().toLocaleTimeString()}] ${message}`;
    logEntry.dataset.originalText = message; // For filtering purposes
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;

    if (filterText && !message.toLowerCase().includes(filterText)) {
        logEntry.style.display = "none";
    }
}

function clearLogs() {
    logContainer.innerHTML = "";
    addLogEntry("🧹 Logs cleared manually.", "info");
}

function togglePauseLogs() {
    isPaused = !isPaused;
    pauseButton.innerText = isPaused ? "Resume Logs" : "Pause Logs";
    addLogEntry(isPaused ? "⏸️ Logs paused." : "▶️ Logs resumed.", "info");
}

function filterLogs() {
    filterText = filterInput.value.toLowerCase();
    const entries = document.querySelectorAll(".log-entry");
    entries.forEach(entry => {
        const message = entry.dataset.originalText.toLowerCase();
        entry.style.display = message.includes(filterText) ? "block" : "none";
    });
}

// Button Event Listeners for Logs
pauseButton.addEventListener("click", togglePauseLogs);
clearButton.addEventListener("click", clearLogs);
filterInput.addEventListener("input", filterLogs);

// =========================
// 📑 WebSocket for Directives
// =========================



// WebSocket for Directive Updates
const directiveSocket = new WebSocket("ws://127.0.0.1:8000/ws/directives");

directiveSocket.onopen = () => {
    console.log("✅ Connected to Directives WebSocket");
    addLogEntry("✅ Connected to Directives WebSocket", "success");
};

directiveSocket.onmessage = (event) => {
    console.log("📡 Raw Directive WebSocket Message:", event.data);

    try {
        const data = JSON.parse(event.data);
        console.log("🔍 Parsed Directive WebSocket Data:", data);

        if (data.type === "directive_update" && data.directive) {
            console.log("✅ Directive Update Detected:", data.directive);
            addLogEntry(`✅ Directive Update: ${JSON.stringify(data.directive)}`, "info");
            updateDirectiveTable(data.directive);
        } else if (data.type === "info") {
            console.log(`📝 Info Message: ${data.message}`);
            addLogEntry(`📝 Info Message: ${data.message}`, "info");
        } else {
            console.warn("⚠️ Unrecognized WebSocket message type:", data);
        }
    } catch (error) {
        console.error("❌ Error parsing directive WebSocket message:", error);
        addLogEntry("❌ Error parsing directive message", "error");
    }
};

directiveSocket.onerror = (error) => {
    console.error("❌ Directives WebSocket Error:", error);
    addLogEntry(`❌ Directives WebSocket Error: ${error}`, "error");
};

directiveSocket.onclose = () => {
    console.warn("🔌 Directives WebSocket Disconnected");
    addLogEntry("🔌 Directives WebSocket Disconnected", "warning");
};



// Update Directive Table
console.log("THIS IS ALL STARTING HERE, lakakakakak");
function updateDirectiveTable(directive) {
    console.log("🔄 Updating Directive Table with:", directive);

    // Get the table body
    const tableBody = document.querySelector("#directiveTable tbody");
    if (!tableBody) {
        console.error("❌ Directive Table body not found in the DOM");
        return;
    }

    // Search for an existing row
    let row = document.querySelector(`#directive-${directive.id}`);

    if (!row) {
        // Create a new row if it doesn't exist
        row = document.createElement("tr");
        row.id = `directive-${directive.id}`;
        row.innerHTML = `
            <td>${directive.id}</td>
            <td>${directive.agent_id}</td>
            <td>${directive.task}</td>
            <td>${directive.status}</td>
        `;
        tableBody.appendChild(row);
        console.log(`✅ New directive row added for ID: ${directive.id}`);
    } else {
        // Update the existing row's status
        row.cells[3].textContent = directive.status;
        console.log(`✅ Directive row updated for ID: ${directive.id}, Status: ${directive.status}`);
    }
}




// =========================
// ⚙️ Utility Functions
// =========================

// Retry Directive
function retryDirective(directiveId) {
    fetch(`/api/retry_directive/${directiveId}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        addLogEntry(`🔄 Retry Directive Response: ${data.message}`, "info");
    })
    .catch(error => {
        addLogEntry(`❌ Retry Directive Failed: ${error}`, "error");
    });
}

// Cancel Directive
function cancelDirective(directiveId) {
    fetch(`/api/cancel_directive/${directiveId}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        addLogEntry(`🛑 Cancel Directive Response: ${data.message}`, "info");
    })
    .catch(error => {
        addLogEntry(`❌ Cancel Directive Failed: ${error}`, "error");
    });
}

// =========================
// 📝 Initialization
// =========================
addLogEntry("🖥️ WebSocket Client Initialized. Awaiting updates...", "info");
console.log("✅ WebSocket Client Initialized.");
