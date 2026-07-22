document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const errorMsg = document.getElementById("errorMsg");
  errorMsg.textContent = "";

  try {
    const data = await apiRequest("/auth/login", "POST", { email, password });
    setToken(data.access_token);
    window.location.href = "dashboard.html";
  } catch (err) {
    errorMsg.textContent = err.message;
  }
});

// Agar already logged in hai, seedha dashboard bhej do
if (getToken()) {
  window.location.href = "dashboard.html";
}