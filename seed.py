import sqlite3
import random
from werkzeug.security import generate_password_hash

DB_PATH = 'skillloop.db'

GRADIENTS = [
    'linear-gradient(135deg, #FF6B6B, #FF8E53)',
    'linear-gradient(135deg, #667eea, #764ba2)',
    'linear-gradient(135deg, #f093fb, #f5576c)',
    'linear-gradient(135deg, #4facfe, #00f2fe)',
    'linear-gradient(135deg, #43e97b, #38f9d7)'
]

users_data = [
    ("alice", "alice@example.com", "Alice Smith", "Computer Science", 4, [("python", "teaches"), ("guitar", "learns")]),
    ("bob99", "bob@example.com", "Bob Johnson", "Music", 2, [("guitar", "teaches"), ("french", "learns")]),
    ("charlie", "charlie@example.com", "Charlie Brown", "Linguistics", 6, [("french", "teaches"), ("python", "learns")]),
    ("dave_dev", "dave@example.com", "Dave Williams", "IT", 3, [("react", "teaches"), ("figma", "learns")]),
    ("eve_design", "eve@example.com", "Eve Davis", "Design", 5, [("figma", "teaches"), ("react", "learns")]),
    ("frank", "frank@example.com", "Frank Miller", "Data Science", 7, [("sql", "teaches"), ("docker", "learns")])
]

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Optional: clear existing data just in case
    cursor.execute('DELETE FROM user_skills')
    cursor.execute('DELETE FROM users')
    
    for user in users_data:
        username, email, full_name, dept, sem, skills = user
        pw_hash = generate_password_hash("password123")
        avatar = random.choice(GRADIENTS)
        
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, department, semester, avatar_color)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, pw_hash, full_name, dept, sem, avatar))
        
        user_id = cursor.lastrowid
        
        for skill_name, skill_type in skills:
            cursor.execute('''
                INSERT INTO user_skills (user_id, skill_name, skill_type)
                VALUES (?, ?, ?)
            ''', (user_id, skill_name, skill_type))
            
    conn.commit()
    conn.close()
    print("Database successfully seeded with fake users and skills!")

if __name__ == '__main__':
    seed()
