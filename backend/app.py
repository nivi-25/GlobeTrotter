from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database/globetrotter.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "GlobeTrotter Backend Running"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (data['name'], data['email'], data['password'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User created successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (data['email'], data['password'])
    ).fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)
