from flask import Flask, request, redirect, url_for, render_template, session, jsonify
import sqlite3
import os
from functools import wraps
from datetime import datetime
import logging
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.secret_key = 'your_secret_key'
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if admin:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM user').fetchall()
    conn.close()
    return render_template('dashboard.html', users=users)

@app.route('/generate_url', methods=['POST'])
@login_required
def generate_url():
    unique_url = os.urandom(16).hex()
    conn = get_db_connection()
    conn.execute('INSERT INTO user (unique_url) VALUES (?)', (unique_url,))
    conn.commit()
    conn.close()
    return jsonify({'unique_url': unique_url})

logging.basicConfig(level=logging.DEBUG)

@app.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        user_id = request.json.get('user_id')
        conn = get_db_connection()
        conn.execute('DELETE FROM user WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return '', 204  # Return HTTP 204 No Content on successful deletion
    except Exception as e:
        print(f"Error deleting user: {e}")
        return 'Failed to delete user', 500  # Return an error response if deletion fails

@app.route('/location/<unique_url>', methods=['GET', 'POST'])
def location(unique_url):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE unique_url = ?', (unique_url,)).fetchone()
    conn.close()
    if request.method == 'POST':
        data = request.json
        conn = get_db_connection()
        # Formatting datetime in AM/PM format
        now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        conn.execute('UPDATE user SET last_latitude = ?, last_longitude = ?, last_update = ? WHERE unique_url = ?',
                     (data['latitude'], data['longitude'], now, unique_url))
        conn.commit()
        conn.close()
        return 'Location updated'
    return render_template('location.html', unique_url=unique_url)

if __name__ == "__main__":
    app.run(debug=True)
