import sqlite3
import datetime
import json

def get_db_connection():
    conn = sqlite3.connect('seletordltsaude.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS recommendations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  scenario TEXT,
                  dlt TEXT,
                  consensus TEXT,
                  timestamp DATETIME)''')

    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  scenario TEXT,
                  dlt TEXT,
                  consensus TEXT,
                  rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                  usefulness TEXT,
                  comment TEXT,
                  specific_aspects TEXT,
                  timestamp DATETIME)''')

    conn.commit()
    conn.close()

def create_user(username, hashed_password):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def save_recommendation(username, scenario, recommendation):
    conn = get_db_connection()
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute("""INSERT INTO recommendations 
                 (username, scenario, dlt, consensus, timestamp) 
                 VALUES (?, ?, ?, ?, ?)""",
              (username, scenario, recommendation['dlt'], 
               recommendation['consensus'], timestamp))
    conn.commit()
    conn.close()

def get_user_recommendations(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT * FROM recommendations 
                 WHERE username = ? 
                 ORDER BY timestamp DESC LIMIT 5""", (username,))
    recommendations = c.fetchall()
    conn.close()
    return recommendations

def save_feedback(username, scenario, dlt, consensus_group, feedback_data):
    conn = get_db_connection()
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute('''INSERT INTO feedback 
                 (username, scenario, dlt, consensus, rating, usefulness, comment, specific_aspects, timestamp) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (username, scenario, dlt, consensus_group,
               feedback_data['rating'], feedback_data['usefulness'], feedback_data['comment'],
               json.dumps(feedback_data['specific_aspects']), timestamp))
    conn.commit()
    conn.close()

def add_specific_aspects_column():
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE feedback ADD COLUMN specific_aspects TEXT")
        conn.commit()
        print("Added 'specific_aspects' column to feedback table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" not in str(e):
            print(f"Error adding 'specific_aspects' column: {e}")
    finally:
        conn.close()

init_db()
add_specific_aspects_column()
