// server calls
async function apiLogin(email, password) {
    const ret = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({email, password})
    });
    if (!res.ok) throw new Error(`Login Failed (${res.status})`);
    return res.json();
}

async function apiListDevices() {
    const res = await fetch(`${API_BASE}/devices`, {
        headers: {"Authorization": `Bearer ${getToken()}`}
    });
    if (!res.ok) throw new Error(`Devices Failed (${res.status})`)
}

async function apiSendCommand() {
    const res = await fetch(`${API_BASE}/commands`, {
        method: "POST",
        headers: {
            "Content-Type" : "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify({ device_id, command, params })

    })
        if (!res.ok) throw new Error(`Command Failed (${res.status})`);
        return res.json();
}