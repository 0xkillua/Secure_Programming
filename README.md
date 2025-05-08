🔐 SQL Injection Lab with Flask
A simple educational lab built using Flask, demonstrating:

💣 SQL Injection vulnerabilities
🚨 Error handling issues
❌ Input validation bypass
✅ Secure coding practices

Perfect for beginners learning about web security, penetration testing, or secure development!

🧪 Features

Page
Description
Security Level



/login-vulnerable
Login form vulnerable to SQL injection, error leaking & weak validation
❌ Insecure


/login-secure
Secure login with parameterized queries, input validation, safe errors
✅ Secure



📦 Requirements
Make sure you have these installed:

🐍 Python 3.x
🧵 Flask (pip install flask)
🗃️ SQLite (comes pre-installed with Python)


📁 Folder Structure
lab_login/
│
├── app.py                  # Main Flask app
├── setup_db.py            # Creates database and sample user
├── templates/
│   ├── login_vulnerable.html  # Template for vulnerable login page
│   ├── login_secure.html      # Template for secure login page
├── static/
│   └── style.css           # Beautiful UI styling
└── README.md               # Project documentation


🚀 Setup Instructions


Install Dependencies:
pip install flask


Create the Database:Run the database setup script to create users.db with a sample user:
python setup_db.py


Start the Flask App:Run the Flask application:
python app.py

The app will be available at http://localhost:5000.



🧪 Usage

Vulnerable Login: Visit http://localhost:5000/login-vulnerable

Try SQL injection (e.g., username: admin' OR '1'='1 and any password) to bypass authentication.
Observe error messages that may leak database details.


Secure Login: Visit http://localhost:5000/login-secure

Attempts at SQL injection will fail due to parameterized queries and input validation.
Error messages are generic and safe.


