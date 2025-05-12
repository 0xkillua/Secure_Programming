from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime, timedelta
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = "0xkillua"

# === VULNERABLE REGISTRATION ===
@app.route('/register-vulnerable', methods=['GET', 'POST'])
def register_vulnerable():
    if request.method == 'POST':
        # No input validation
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthday = request.form['birthday']

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            query = f'''
                INSERT INTO users (username, password, email, first_name, last_name, birthday)
                VALUES ('{username}', '{password}', '{email}', '{first_name}', '{last_name}', '{birthday}')
            '''
            cursor.execute(query)
            conn.commit()
            conn.close()
            flash("🎉 Account created (vulnerable)! Login now.", "success")
            return redirect(url_for('login_vulnerable'))

        except Exception as e:
            flash(f"💀 Error: {str(e)}", "error")

    return render_template('register_vulnerable.html')

# === VALIDATION FUNCTIONS ===
def is_valid_email(email):
    return re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None

def is_valid_username(username):
    if len(username) < 3 or len(username) > 20:
        return False
    if not re.fullmatch(r'^[a-zA-Z0-9][a-zA-Z0-9_]*[a-zA-Z0-9]$', username):
        return False  # No leading/trailing underscores
    if '__' in username:
        return False  # No double underscores
    return True

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):   # At least one uppercase
        return False
    if not re.search(r'[a-z]', password):   # At least one lowercase
        return False
    if not re.search(r'\d', password):      # At least one digit
        return False
    return True

def is_valid_birthday(birthday_str):
    try:
        birth_date = datetime.strptime(birthday_str, '%Y-%m-%d')
        today = datetime.today()
        ten_years_ago = today - timedelta(days=365 * 10)

        if birth_date > today:
            flash("❌ Birthday cannot be in the future.", "error")
            return False
        if birth_date > ten_years_ago:
            flash("❌ You must be at least 10 years old.", "error")
            return False
        return True
    except ValueError:
        flash("❌ Invalid date format.", "error")
        return False

# === SECURE REGISTRATION ROUTE ===
@app.route('/register-secure', methods=['GET', 'POST'])
def register_secure():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthday = request.form['birthday']

        # Input validation
        if not is_valid_username(username):
            flash("❌ Invalid username: 3–20 characters, no special chars or repeated underscores.", "error")
            return redirect(url_for('register_secure'))

        if not is_valid_password(password):
            flash("❌ Password must be at least 8 characters and include uppercase, lowercase, and number.", "error")
            return redirect(url_for('register_secure'))

        if not is_valid_email(email):
            flash("❌ Invalid email address.", "error")
            return redirect(url_for('register_secure'))

        if not is_valid_birthday(birthday):
            return redirect(url_for('register_secure'))

        # Hash password
        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # Check if username or email already exists
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                if existing_user[1] == username:
                    flash("❌ Username already taken.", "error")
                else:
                    flash("❌ Email already registered.", "error")
                return redirect(url_for('register_secure'))

            # Safe insert
            cursor.execute('''
                INSERT INTO users (username, password, email, first_name, last_name, birthday)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, email, first_name, last_name, birthday))

            conn.commit()
            conn.close()

            flash("✅ Account created securely! Login now.", "success")
            return redirect(url_for('login_secure'))

        except Exception as e:
            flash("⚠️ An error occurred. Please try again later.", "error")
            print(f"Database error: {e}")

    return render_template('register_secure.html')
# === VULNERABLE LOGIN ===
@app.route('/login-vulnerable', methods=['GET', 'POST'])
def login_vulnerable():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()

            if user:
                flash("🎉 You cracked the lab!", "success")
            else:
                flash("❌ Invalid credentials.", "error")

        except Exception as e:
            flash(f"💀 Database error: {str(e)}", "error")

    return render_template('login_vulnerable.html')


# === SECURE LOGIN ===
@app.route('/login-secure', methods=['GET', 'POST'])
def login_secure():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not is_valid_username(username):
            flash("Invalid username format.", "error")
            return redirect(url_for('login_secure'))

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            conn.close()

            if user and check_password_hash(user[2], password):  # user[2] is password field
                flash("✅ Login successful!", "success")
            else:
                flash("❌ Invalid credentials.", "error")

        except Exception as e:
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