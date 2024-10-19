import sqlite3
import datetime
import json

# Conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('seletordltsaude.db')
    conn.row_factory = sqlite3.Row  # Para retorno de resultados no formato de dicionário
    return conn

# Inicialização do banco de dados
def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Tabela de usuários
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password TEXT)''')

    # Tabela de recomendações
    c.execute('''CREATE TABLE IF NOT EXISTS recommendations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  scenario TEXT,
                  dlt TEXT,
                  consensus TEXT,
                  timestamp DATETIME)''')

    # Tabela de feedbacks (atualizada)
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

# Função para criar novo usuário
def create_user(username, hashed_password):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:  # Caso o usuário já exista
        return False
    finally:
        conn.close()

# Função para buscar um usuário
def get_user(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

# Função para salvar uma recomendação
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

# Função para buscar recomendações de um usuário
def get_user_recommendations(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT * FROM recommendations 
                 WHERE username = ? 
                 ORDER BY timestamp DESC LIMIT 5""", (username,))
    recommendations = c.fetchall()
    conn.close()
    return recommendations

# Função atualizada para salvar feedback do usuário
def save_feedback(username, scenario, recommendation, feedback_data):
    conn = get_db_connection()
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute("""INSERT INTO feedback 
                 (username, scenario, dlt, consensus, rating, usefulness, comment, specific_aspects, timestamp) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (username, scenario, recommendation['dlt'], recommendation['consensus'],
               feedback_data['rating'], feedback_data['usefulness'], feedback_data['comment'],
               json.dumps(feedback_data['specific_aspects']), timestamp))
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao iniciar a aplicação
init_db()
