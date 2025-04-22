import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "mydata.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check if users table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cur.fetchone():
        print("Creating users table...")
        cur.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)

        # Add a test user (username: test, password: test1234)
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        test_password_hash = bcrypt.generate_password_hash("test1234").decode('utf-8')
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("test", test_password_hash))
        conn.commit()
        print("Test user created")

    # Check if other tables exist
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='doctors'")
    if cur.fetchone():
        return  # If doctors table exists, assume all tables exist

    cur.execute("""
        CREATE TABLE doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            seniority_id INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE seniority (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seniority_name TEXT NOT NULL,
            max_shifts_per_month INTEGER NOT NULL,
            shift_area_ids TEXT,
            shift_duration TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE shift_areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_name TEXT NOT NULL,
            min_doctors_per_area INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE schedule_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_data_name TEXT NOT NULL,
            schedule_data TEXT,
            first_day TEXT,
            days_in_month INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_data_id INTEGER NOT NULL,
            schedule TEXT,
            fitness_score REAL,
            log_messages TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
