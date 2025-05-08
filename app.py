from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re

app = Flask(__name__)
app.secret_key = "0xkillua"

# === VULNERABLE LOGIN ===
@app.route('/login-vulnerable', methods=['GET', 'POST'])
def login_vulnerable():
    if request.method == 'POST':
        # No input validation (Vulnerable)
        username = request.form['username']
        password = request.form['password']

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # 💀 Vulnerable SQL query - SQL Injection possible
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            cursor.execute(query)  # No parameterization

            user = cursor.fetchone()
            conn.close()

            if user:
                flash("🎉 You cracked the lab!", "success")
            else:
                flash("❌ Invalid credentials.", "error")

        except Exception as e:
            # 🚨 Leaking full error message
            flash(f"💀 Database error: {str(e)}", "error")

    return render_template('login_vulnerable.html')


# === SECURE LOGIN LOGIC ===
def is_valid_username(username):
    # ✅ Strong input validation
    return re.fullmatch(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

def is_valid_password(password):
    return len(password) >= 6

@app.route('/login-secure', methods=['GET', 'POST'])
def login_secure():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ✅ Input validation
        if not is_valid_username(username):
            flash("Invalid username format.", "error")
            return redirect(url_for('login_secure'))
        if not is_valid_password(password):
            flash("Password must be at least 6 characters.", "error")
            return redirect(url_for('login_secure'))

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # ✅ Secure parameterized query
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                flash("✅ Login successful!", "success")
            else:
                flash("❌ Invalid credentials.", "error")

        except Exception as e:
            # ✅ Generic error shown
            flash("An error occurred. Please try again later.", "error")

    return render_template('login_secure.html')


# === Home Redirects ===
@app.route('/')
def index_vulnerable():
    return redirect(url_for('login_vulnerable'))

@app.route('/secure')
def index_secure():
    return redirect(url_for('login_secure'))


if __name__ == '__main__':
    app.run(debug=True)