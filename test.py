import os
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Vulnerable to SQL Injection
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Vulnerable: using string formatting in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

# Vulnerable to Command Injection
def backup_data(filename):
    # Vulnerable: using user input directly in command
    os.system(f"tar -czf /tmp/backup.tar.gz {filename}")
    return "Backup completed"

# Vulnerable to XSS
@app.route('/profile')
def profile():
    # Vulnerable: directly using user input in HTML
    name = request.args.get('name', '')
    template = f"<h1>Hello, {name}!</h1>"
    return render_template_string(template)

# Vulnerable to Path Traversal
@app.route('/download')
def download_file():
    # Vulnerable: no path validation
    filename = request.args.get('filename')
    with open(filename, 'r') as f:
        content = f.read()
    return content

if __name__ == "__main__":
    app.run(debug=True) 
