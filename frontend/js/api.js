const API_BASE = "https://secureidentity-backend.onrender.com"; // backend live URL (After deployed it on render)

function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function clearToken() {
  localStorage.removeItem("access_token");
}

async function apiRequest(endpoint, method = "GET", body = null) {
  const headers = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const config = { method, headers };
  if (body) config.body = JSON.stringify(body);

  const response = await fetch(`${API_BASE}${endpoint}`, config);
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    // Sirf tab redirect karo jab already logged-in user ka token invalid ho
    // Login route khud pe 401 aana galat credentials ka matlab hai, redirect nahi
    if (response.status === 401 && !endpoint.includes("/auth/login")) {
      clearToken();
      window.location.href = "index.html";
    }
    throw new Error(data?.detail || "Something went wrong");
  }
  return data;
}