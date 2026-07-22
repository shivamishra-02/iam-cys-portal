let currentUser = null;

async function init() {
  if (!getToken()) {
    window.location.href = "index.html";
    return;
  }

  try {
    currentUser = await apiRequest("/employee/profile");
    renderProfile();
    setupRoleVisibility();
    loadCommonData();
  } catch (err) {
    console.error(err);
  }
}

function renderProfile() {
  document.getElementById("userInfo").textContent = `${currentUser.full_name} (${currentUser.role})`;
  document.getElementById("profileBox").innerHTML = `
    <p><strong>Name:</strong> ${currentUser.full_name}</p>
    <p><strong>Email:</strong> ${currentUser.email}</p>
    <p><strong>Role:</strong> <span class="badge badge-${currentUser.role}">${currentUser.role}</span></p>
    <p><strong>Status:</strong> <span class="badge badge-${currentUser.is_active ? 'active' : 'inactive'}">${currentUser.is_active ? 'Active' : 'Inactive'}</span></p>
  `;
  document.getElementById("editFullName").value = currentUser.full_name;
  document.getElementById("editEmail").value = currentUser.email;
}

function setupRoleVisibility() {
  if (currentUser.role === "manager" || currentUser.role === "admin") {
    document.querySelectorAll(".manager-only").forEach(el => el.classList.remove("hidden"));
  }
  if (currentUser.role === "admin") {
    document.querySelectorAll(".admin-only").forEach(el => el.classList.remove("hidden"));
  }
}

function loadCommonData() {
  if (currentUser.role === "manager" || currentUser.role === "admin") {
    loadEmployees();
    loadAccessRequests();
  }
  if (currentUser.role === "admin") {
    loadAllUsers();
    loadAuditLogs();
  }
}

function toggleForm(id) {
  document.getElementById(id).classList.toggle("hidden-form");
}

/* ===== EMPLOYEE ACTIONS ===== */

document.getElementById("editProfileForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const full_name = document.getElementById("editFullName").value;
  const email = document.getElementById("editEmail").value;
  try {
    currentUser = await apiRequest("/employee/profile", "PUT", { full_name, email });
    renderProfile();
    alert("Profile updated!");
  } catch (err) {
    alert(err.message);
  }
});

document.getElementById("changePasswordForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const old_password = document.getElementById("oldPassword").value;
  const new_password = document.getElementById("newPassword").value;
  const msg = document.getElementById("passwordMsg");
  try {
    await apiRequest(`/employee/change-password?old_password=${encodeURIComponent(old_password)}&new_password=${encodeURIComponent(new_password)}`, "POST");
    msg.textContent = "Password changed successfully!";
    e.target.reset();
  } catch (err) {
    msg.textContent = err.message;
    msg.style.color = "#f87171";
  }
});

document.getElementById("accessRequestForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const resource_name = document.getElementById("resourceName").value;
  const reason = document.getElementById("reason").value;
  const msg = document.getElementById("accessMsg");
  try {
    await apiRequest("/employee/request-access", "POST", { resource_name, reason });
    msg.textContent = "Access request submitted!";
    e.target.reset();
  } catch (err) {
    msg.textContent = err.message;
  }
});

/* ===== MANAGER ACTIONS ===== */

async function loadEmployees() {
  const employees = await apiRequest("/manager/employees");
  const box = document.getElementById("employeeList");
  box.innerHTML = `<table><tr><th>Name</th><th>Email</th><th>Status</th></tr>` +
    employees.map(emp => `
      <tr>
        <td>${emp.full_name}</td>
        <td>${emp.email}</td>
        <td><span class="badge badge-${emp.is_active ? 'active' : 'inactive'}">${emp.is_active ? 'Active' : 'Inactive'}</span></td>
      </tr>
    `).join("") + `</table>`;
}

async function loadAccessRequests() {
  const requests = await apiRequest("/manager/access-requests");
  const box = document.getElementById("accessRequestsList");
  box.innerHTML = `<table><tr><th>Resource</th><th>Reason</th><th>Status</th><th>Action</th></tr>` +
    requests.map(r => `
      <tr>
        <td>${r.resource_name}</td>
        <td>${r.reason || "-"}</td>
        <td><span class="badge badge-${r.status}">${r.status}</span></td>
        <td>
          ${r.status === "pending" ? `
            <button class="action-btn btn-approve" onclick="reviewRequest(${r.id}, 'approved')">Approve</button>
            <button class="action-btn btn-reject" onclick="reviewRequest(${r.id}, 'rejected')">Reject</button>
          ` : "-"}
        </td>
      </tr>
    `).join("") + `</table>`;
}

async function reviewRequest(id, status) {
  try {
    await apiRequest(`/manager/access-requests/${id}`, "PATCH", { status });
    loadAccessRequests();
  } catch (err) {
    alert(err.message);
  }
}

/* ===== ADMIN ACTIONS ===== */

document.getElementById("createUserForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const full_name = document.getElementById("newFullName").value;
  const email = document.getElementById("newEmail").value;
  const password = document.getElementById("newPassword2").value;
  const role = document.getElementById("newRole").value;
  const msg = document.getElementById("createUserMsg");
  try {
    await apiRequest("/admin/users/", "POST", { full_name, email, password, role });
    msg.textContent = "User created successfully!";
    e.target.reset();
    loadAllUsers();
  } catch (err) {
    msg.textContent = err.message;
    msg.style.color = "#f87171";
  }
});

async function loadAllUsers() {
  const users = await apiRequest("/admin/users/");
  const box = document.getElementById("allUsersList");
  box.innerHTML = `<table><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Actions</th></tr>` +
    users.map(u => `
      <tr>
        <td>${u.full_name}</td>
        <td>${u.email}</td>
        <td><span class="badge badge-${u.role}">${u.role}</span></td>
        <td><span class="badge badge-${u.is_active ? 'active' : 'inactive'}">${u.is_active ? 'Active' : 'Inactive'}</span></td>
        <td>
          ${u.is_active
            ? `<button class="action-btn btn-deactivate" onclick="toggleActive(${u.id}, false)">Deactivate</button>`
            : `<button class="action-btn btn-activate" onclick="toggleActive(${u.id}, true)">Activate</button>`
          }
          <button class="action-btn btn-delete" onclick="deleteUser(${u.id})">Delete</button>
        </td>
      </tr>
    `).join("") + `</table>`;
}

async function toggleActive(id, activate) {
  try {
    await apiRequest(`/admin/users/${id}/${activate ? 'activate' : 'deactivate'}`, "PATCH");
    loadAllUsers();
  } catch (err) {
    alert(err.message);
  }
}

async function deleteUser(id) {
  if (!confirm("Are you sure you want to delete this user?")) return;
  try {
    await apiRequest(`/admin/users/${id}`, "DELETE");
    loadAllUsers();
  } catch (err) {
    alert(err.message);
  }
}

async function loadAuditLogs() {
  const logs = await apiRequest("/admin/users/audit-logs");
  const box = document.getElementById("auditLogsList");
  box.innerHTML = `<table><tr><th>Action</th><th>Details</th><th>Time</th></tr>` +
    logs.map(l => `
      <tr>
        <td>${l.action}</td>
        <td>${l.details || "-"}</td>
        <td>${new Date(l.timestamp).toLocaleString()}</td>
      </tr>
    `).join("") + `</table>`;
}

/* ===== LOGOUT ===== */
document.getElementById("logoutBtn").addEventListener("click", () => {
  clearToken();
  window.location.href = "index.html";
});

init();