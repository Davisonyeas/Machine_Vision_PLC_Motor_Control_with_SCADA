// Login credentials for user, fetting from browser cache

// Use current host + port 8000 for API
const API_BASE = `http://${window.location.hostname}:8000/api/v1`
const TOKEN_KEY = "access_token"

// read save token from the brwoser
const getToken = () => localStorage.getItem(TOKEN_KEY) || "";
// save token to stay logged in after refresh
const setToken = (t) => {
    if (t) localStorage.setItem(TOKEN_KEY, t);
    else localStorage.removeItem(TOKEN_KEY);
};