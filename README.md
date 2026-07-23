# 🔐 SecureIdentity — Identity & Access Management Portal

A full-stack **Identity & Access Management (IAM)** system built to demonstrate core enterprise security concepts: authentication, role-based access control (RBAC), least privilege, user provisioning/deprovisioning, and audit logging.

Built as a hands-on project to apply real-world IAM and cybersecurity principles using a modern backend/frontend stack.

---

## 📌 Features

### Authentication
- Secure login with JWT (JSON Web Tokens)
- Passwords hashed with bcrypt (never stored in plain text)
- Stateless token-based session management
- Logout (client-side token invalidation)

### Role-Based Access Control (RBAC)
Three roles with distinct permissions:

| Role | Permissions |
|------|-------------|
| **Admin** | Create/edit/delete users, activate/deactivate accounts, assign roles, reset passwords, view audit logs |
| **Manager** | View employees, approve/reject access requests |
| **Employee** | View/update own profile, change password, request access to resources |

### Audit Logging
Every sensitive action is logged with timestamp and actor:
- Login events
- User creation / deletion
- Role changes
- Password changes
- Access request approvals/rejections

### IAM Concepts Demonstrated
- **Authentication** — verifying identity via credentials + JWT
- **Authorization** — enforcing what an authenticated user is allowed to do
- **RBAC** — permissions scoped to roles, not individuals
- **Least Privilege** — employees request access rather than receiving it by default
- **Provisioning / Deprovisioning** — admin-controlled user lifecycle (create, activate, deactivate, delete)
- **Audit Logging** — traceable record of security-relevant events

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, Vanilla JavaScript |
| Backend | FastAPI (Python) |
| Database | SQLite |
| ORM | SQLAlchemy |
| Authentication | JWT (python-jose) |
| Password Hashing | bcrypt (Passlib) |
| Validation | Pydantic |
| API Testing | Postman / Swagger UI |

---

## 🏗️ Architecture

```
Client (HTML/CSS/JS)
        │  HTTP requests (JSON)
        ▼
FastAPI Routes  (routes/)
        │
        ▼
Service Layer   (services/)   ← business logic, RBAC checks, audit logging
        │
        ▼
SQLAlchemy Models (models/)
        │
        ▼
SQLite Database
```

**Why this structure?**
Routes only handle HTTP concerns. Services contain business logic. Models define data structure. This separation keeps the codebase testable, maintainable, and mirrors how production backend systems are organized.

---

## 📁 Project Structure

```
iam-cys-portal/
├── backend/
│   ├── app/
│   │   ├── core/            # Config, security (JWT, hashing), dependencies
│   │   ├── db/               # Database connection/session
│   │   ├── models/           # SQLAlchemy tables (User, AuditLog, AccessRequest)
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── services/         # Business logic layer
│   │   ├── routes/           # API endpoints (auth, users, manager, employee)
│   │   └── main.py           # FastAPI entrypoint
│   ├── requirements.txt
│   └── .env                  # Environment variables (not committed)
├── frontend/
│   ├── css/style.css
│   ├── js/api.js
│   ├── js/login.js
│   ├── js/dashboard.js
│   ├── index.html            # Login page
│   └── dashboard.html        # Role-based dashboard
└── README.md
```

---

## 🚀 Running Locally

### Prerequisites
- Python 3.11+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/shivamishra-02/iam-cys-portal.git
cd iam-cys-portal
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
DATABASE_URL=sqlite:///./secureidentity.db
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Backend will be live at:
- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup

The frontend is plain HTML/CSS/JS — no build step required.

**Option A — Open directly**
Just double-click `frontend/index.html` to open it in your browser.

**Option B — Use a local server (recommended)**
Some browsers restrict `fetch()` calls from `file://` pages. Serving it avoids that:

```bash
cd frontend
python3 -m http.server 5500
```

Then open: `http://127.0.0.1:5500`

> If using VS Code, the **Live Server** extension works too — right-click `index.html` → "Open with Live Server".

### 4. Connect Frontend to Backend

In `frontend/js/api.js`, the `API_BASE` constant points to the backend:

```javascript
const API_BASE = "http://127.0.0.1:8000";
```

Keep this as-is for local development. Update it only after deploying the backend (see below).

### 5. First Login

Since there's no public signup (admin-provisioned accounts only, by design), create your first admin user directly via Swagger UI (`/docs`) or by temporarily using the `/admin/users/` endpoint with a manually inserted first admin — see [Creating the First Admin](#-creating-the-first-admin) below.

---

## 👤 Creating the First Admin

Since every `/admin/users/` route requires an existing admin token, you need one manual bootstrap step the very first time:

```bash
cd backend
source venv/bin/activate
python3
```

```python
from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()
admin = User(
    full_name="Super Admin",
    email="admin@secureidentity.com",
    hashed_password=hash_password("Admin@123"),
    role="admin",
    is_active=True
)
db.add(admin)
db.commit()
db.close()
```

Now log in with `admin@secureidentity.com` / `Admin@123` — from there, use the dashboard's **Create User** form to provision Managers and Employees.

---

## 🔒 Security Notes

- Passwords are never stored or transmitted in plain text
- JWTs are signed with a secret key and expire after a configurable window
- Deactivated users are blocked at both login and token-validation time — revoking access takes effect immediately, not just at token expiry
- API error messages for login avoid confirming whether an email exists, to prevent user enumeration attacks
- `.env` and the SQLite database file are excluded from version control via `.gitignore`

---

## 🗺️ Roadmap Ideas (not implemented, for future extension)

- Refresh tokens
- Multi-factor authentication (MFA)
- Password complexity enforcement + expiry policies
- Email notifications for access request outcomes
- PostgreSQL for production deployments

---

## 📄 License

This project was built for educational and portfolio purposes.