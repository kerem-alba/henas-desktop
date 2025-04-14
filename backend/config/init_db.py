import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "mydata.db")

def init_db():
    if os.path.exists(DB_PATH):
        return  # zaten varsa atla

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

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
