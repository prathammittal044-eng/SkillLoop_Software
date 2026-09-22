import sqlite3
from flask import g
from config import Config

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(Config.DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(Config.DATABASE)
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            department TEXT,
            semester INTEGER,
            bio TEXT,
            education TEXT,
            qualifications TEXT,
            experience TEXT,
            github TEXT,
            linkedin TEXT,
            avatar_color TEXT NOT NULL,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            streak_count INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            time_credits REAL DEFAULT 5.0,
            total_sessions INTEGER DEFAULT 0,
            skills_taught INTEGER DEFAULT 0,
            skills_learned INTEGER DEFAULT 0,
            rating_avg REAL DEFAULT 0.0,
            rating_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS user_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            skill_type TEXT NOT NULL, -- 'teaches' or 'learns'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, skill_name, skill_type)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending', -- 'pending', 'accepted', 'rejected'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (requester_id) REFERENCES users (id),
            FOREIGN KEY (receiver_id) REFERENCES users (id),
            UNIQUE(requester_id, receiver_id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            passed BOOLEAN NOT NULL,
            xp_earned INTEGER NOT NULL,
            tab_switches INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS skill_verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            verified_level TEXT NOT NULL,
            verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activity_type TEXT DEFAULT 'quiz',
            sessions_taught INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, skill_name)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS aee_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            learner_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            duration_minutes INTEGER DEFAULT 30,
            topic_notes TEXT DEFAULT '',
            status TEXT DEFAULT 'pending', -- 'pending', 'confirmed', 'rejected'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            confirmed_at TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES users(id),
            FOREIGN KEY (learner_id) REFERENCES users(id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS user_resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            target_role TEXT DEFAULT '',
            summary TEXT DEFAULT '',
            experiences TEXT DEFAULT '[]',
            education TEXT DEFAULT '[]',
            certifications TEXT DEFAULT '[]',
            projects TEXT DEFAULT '[]',
            custom_skills TEXT DEFAULT '[]',
            settings TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Safe schema migration for existing databases
    cursor = db.cursor()
    cursor.execute("PRAGMA table_info(skill_verifications)")
    existing_cols = [row[1] for row in cursor.fetchall()]
    if 'last_activity_at' not in existing_cols:
        cursor.execute("ALTER TABLE skill_verifications ADD COLUMN last_activity_at TIMESTAMP")
        cursor.execute("UPDATE skill_verifications SET last_activity_at = COALESCE(verified_at, datetime('now')) WHERE last_activity_at IS NULL")
    if 'activity_type' not in existing_cols:
        cursor.execute("ALTER TABLE skill_verifications ADD COLUMN activity_type TEXT DEFAULT 'quiz'")
    if 'sessions_taught' not in existing_cols:
        cursor.execute("ALTER TABLE skill_verifications ADD COLUMN sessions_taught INTEGER DEFAULT 0")

    db.commit()
    db.close()

