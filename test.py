import os
import sqlite3
from flask import Flask, request, render_template_string
import tarfile

app = Flask(__name__)

# Vulnerable to SQL Injection
# Cachebust
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Secure: use parameterized query to prevent SQL injection
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()

# Vulnerable to Command Injection
def backup_data(filename):
    # Only allow backup of specific files (whitelist)
    allowed_files = {'data.txt', 'important.log'}
    if filename not in allowed_files:
        return "Invalid filename"
    # Use tarfile for safer archiving
    with tarfile.open('/tmp/backup.tar.gz', 'w:gz') as tar:
        tar.add(filename)
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
    # Secure: restrict file access to a specific directory and prevent path traversal
    BASE_DIR = '/tmp/allowed_files'  # Change this to your allowed directory
    filename = request.args.get('filename')
    if not filename:
        return 'Filename required', 400
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(BASE_DIR, safe_filename)
    if not os.path.abspath(filepath).startswith(os.path.abspath(BASE_DIR)):
        return 'Invalid filename', 400
    if not os.path.exists(filepath):
        return 'File not found', 404
    with open(filepath, 'r') as f:
        content = f.read()
    return content

if __name__ == "__main__":
    app.run(debug=True) 
