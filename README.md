# 🔐 SQL Injection Lab with Flask

A simple educational lab built using **Flask**, demonstrating:

- 💣 SQL Injection vulnerabilities  
- 🚨 Error handling issues  
- ❌ Input validation bypass  
- ✅ Secure coding practices  

Perfect for **beginners** learning about **web security**, **penetration testing**, or **secure development**!

---

## 🧪 Features

| Page                | Description                                                                 | Security Level |
|---------------------|-----------------------------------------------------------------------------|----------------|
| `/login-vulnerable` | Login form vulnerable to SQL injection, error leaking & weak validation     | ❌ Insecure     |
| `/login-secure`     | Secure login with parameterized queries, input validation, safe error handling | ✅ Secure       |

---

## 📦 Requirements

Make sure you have these installed:

- 🐍 Python 3.x  
- 🧵 Flask (`pip install flask`)  
- 🗃️ SQLite (comes pre-installed with Python)

---

## 🛠️ Setup Instructions

### 1. Install Flask (if not already installed)

```bash
pip install flask
```

### 2. Create the Database 
```bash
python3 setup_db.py
```
### 3.  Start the Flask Application
```bash
python3 app.py
```
### 4. 🔎 Access the App
The app will be available at:
👉 http://localhost:5000
Thank you
11
