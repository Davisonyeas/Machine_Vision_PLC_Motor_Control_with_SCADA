const authStatusEl   = document.getElementById("authStatus");
const emailEl        = document.getElementById("email");
const passwordEl     = document.getElementById("password");
const loginBtn       = document.getElementById("loginBtn");
const logoutBtn      = document.getElementById("logoutBtn");

const loadDevicesBtn = document.getElementById("loadDevicesBtn");
const devicesOutput  = document.getElementById("devicesOutput");

const sendCommandBtn = document.getElementById("sendCommandBtn");
const deviceIdEl     = document.getElementById("deviceId");
const commandNameEl  = document.getElementById("commandName");
const commandOutput  = document.getElementById("commandOutput");

function setAuthStatus() {
  authStatusEl.textContent = getToken() ? "Logged in" : "Not logged in";
}

loginBtn.addEventListener("click", async () => {
  try {
    const data = await apiLogin(emailEl.value.trim(), passwordEl.value);
    setToken(data.access_token);
    setAuthStatus();
    alert("Logged in!");
  } catch (err) {
    alert(err.message);
  }
});

logoutBtn.addEventListener("click", () => {
  setToken("");
  setAuthStatus();
  alert("Logged out.");
});

loadDevicesBtn.addEventListener("click", async () => {
  if (!getToken()) return alert("Login first.");
  try {
    const devices = await apiListDevices();
    devicesOutput.textContent = JSON.stringify(devices, null, 2);
    if (devices.length) deviceIdEl.value = devices[0].id;
  } catch (err) {
    alert(err.message);
  }
});

sendCommandBtn.addEventListener("click", async () => {
  if (!getToken()) return alert("Login first.");
  const device_id = deviceIdEl.value.trim();
  const command   = commandNameEl.value.trim();
  if (!device_id || !command) return alert("Fill device_id and command.");
  try {
    const resp = await apiSendCommand(device_id, command, { speed: 50 });
    commandOutput.textContent = JSON.stringify(resp, null, 2);
  } catch (err) {
    alert(err.message);
  }
});

// on load
setAuthStatus();

// Recognition UI elements
const recognitionNameEl = document.getElementById("recognitionName");
const recognitionStatusEl = document.getElementById("recognitionStatus");

// Poll the backend recognition status endpoint every 1s and update the UI
async function fetchRecognitionStatus() {
  if (!recognitionNameEl || !recognitionStatusEl) return;
  try {
    const res = await fetch(`${API_BASE}/recognition/status`);
    if (!res.ok) throw new Error(`status ${res.status}`);
    const data = await res.json();
    recognitionNameEl.textContent = data.name || "Unknown";
    recognitionStatusEl.textContent = data.status || "idle";
  } catch (err) {
    console.error("Recognition fetch error:", err, "URL:", `${API_BASE}/recognition/status`);
    recognitionNameEl.textContent = "No Connection";
    recognitionStatusEl.textContent = "offline";
  }
}

setInterval(fetchRecognitionStatus, 1000);
fetchRecognitionStatus();
