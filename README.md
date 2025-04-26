
# Work Log Portal – Backend (FastAPI + PostgreSQL)

This is the backend API service for the Work Log Portal project, built with **FastAPI**, **PostgreSQL**, and **JWT authentication**.

---

## 🔧 Requirements

- Python 3.9+
- PostgreSQL running on port 5434
- (Optional) Node.js for React frontend

---

## 📦 Setup Instructions

### 1. Clone the repo and navigate to the backend directory

```bash
git clone <repo-url>
cd Work_log_Portal
```

### 2. Create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Alternatively, install manually:
```bash
pip install fastapi "uvicorn[standard]" sqlalchemy psycopg2-binary \
    python-jose[cryptography] passlib[bcrypt] python-dotenv email-validator
```

---

### 4. Prepare your `.env` file

Create a `.env` based on `.env.template`:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5434
DATABASE_NAME=internlogdb
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 5. Run database migrations / create tables

```bash
python create_tables.py
```

---

### 6. Start the backend server

```bash
./start_backend.sh
```

Then open Swagger UI at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 API Testing Flow

1. Call `/register` with JSON to create an account
2. Call `/login` with JSON:
   ```json
   {
     "email": "test@example.com",
     "password": "strongpass123"
   }
   ```
3. Copy the returned token and click "Authorize" in Swagger UI  
   Paste it as: `Bearer <your-token>`
4. Call `/me` to verify login

---

## 🧠 Notes

- Port used for PostgreSQL is **5434**
- All authentication uses **JWT Bearer Token**
- `/login` now supports **JSON input** instead of form-data
