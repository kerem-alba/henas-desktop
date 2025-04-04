import psycopg2
import json
import os
import config.globals as g
from flask_bcrypt import Bcrypt
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()

import sqlite3

bcrypt = Bcrypt()


DB_PATH = os.path.join(os.path.dirname(__file__), "mydata.db")

def connect_to_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def authenticate_user(username, password):
    auth_conn = psycopg2.connect(os.getenv("AUTH_DB_URL"), sslmode="disable")
    auth_cur = auth_conn.cursor(cursor_factory=RealDictCursor)

    auth_cur.execute("SELECT id, password_hash, hospital_db_name FROM users WHERE username = %s", (username,))
    user = auth_cur.fetchone()

    auth_cur.close()
    auth_conn.close()

    if user and bcrypt.check_password_hash(user["password_hash"], password):
        g.hospital_db_name = user["hospital_db_name"]
        return {"user_id": user["id"], "hospital_db": g.hospital_db_name}

    return None


def get_detailed_doctors():
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT d.name, d.seniority_id, s.max_shifts_per_month, s.shift_area_ids
        FROM doctors d
        JOIN seniority s ON d.seniority_id = s.id
        ORDER BY d.id
    """)
    rows = cur.fetchall()
    conn.close()

    doctors = []
    for row in rows:
        name = row["name"]
        seniority_id = row["seniority_id"]
        max_shifts = row["max_shifts_per_month"]
        shift_area_ids = json.loads(row["shift_area_ids"]) if row["shift_area_ids"] else []
        doctors.append((name, seniority_id, max_shifts, shift_area_ids))

    return doctors

def get_doctors():
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT d.id, d.name, s.seniority_name
        FROM doctors d
        INNER JOIN seniority s ON d.seniority_id = s.id
        ORDER BY d.id
    """)
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "seniority_name": row["seniority_name"]
        }
        for row in rows
    ]

def add_doctor(data):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO doctors (name, seniority_id) VALUES (?, ?)",
        (data["name"], data["seniority_id"])
    )
    conn.commit()
    new_id = cur.lastrowid  # Otomatik ID'yi al
    conn.close()

    return new_id

def update_all_doctors(data):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        for doctor in data:
            cur.execute(
                """
                UPDATE doctors
                SET name = ?,
                    seniority_id = ?
                WHERE id = ?
                """,
                (doctor["name"], doctor["seniority_id"], doctor["id"]),
            )

        conn.commit()
        conn.close()

    except Exception as e:
        print("update_all_doctors fonksiyonunda hata:", e)
        raise

def delete_doctor(doctor_id):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    conn.commit()
    conn.close()


def get_seniority():
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT id, seniority_name, max_shifts_per_month, shift_area_ids, shift_duration
        FROM seniority
        ORDER BY id
    """)
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "seniority_name": row["seniority_name"],
            "max_shifts_per_month": row["max_shifts_per_month"],
            "shift_area_ids": json.loads(row["shift_area_ids"]) if row["shift_area_ids"] else [],
            "shift_duration": row["shift_duration"]
        }
        for row in rows
    ]

def get_detailed_seniority():
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT s.id, s.seniority_name, s.max_shifts_per_month, s.shift_area_ids, s.shift_duration
        FROM seniority s
        ORDER BY s.id
    """)
    rows = cur.fetchall()
    conn.close()

    seniority_list = []
    for row in rows:
        area_ids = json.loads(row["shift_area_ids"]) if row["shift_area_ids"] else []
        seniority_list.append({
            "id": row["id"],
            "seniority_name": row["seniority_name"],
            "max_shifts_per_month": row["max_shifts_per_month"],
            "shift_duration": row["shift_duration"],
            "shift_area_names": [],
            "shift_area_ids": area_ids
        })

    return seniority_list

def add_seniority(data):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO seniority (seniority_name, max_shifts_per_month, shift_area_ids, shift_duration)
        VALUES (?, ?, ?, ?)
    """, (
        data["seniority_name"],
        data["max_shifts_per_month"],
        json.dumps(data["shift_area_ids"]),
        data["shift_duration"]
    ))

    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return new_id

def update_all_seniorities(data):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        for seniority in data:
            cur.execute("""
                UPDATE seniority
                SET seniority_name = ?,
                    max_shifts_per_month = ?,
                    shift_area_ids = ?,
                    shift_duration = ?
                WHERE id = ?
            """, (
                seniority["seniority_name"],
                seniority["max_shifts_per_month"],
                json.dumps(seniority["shift_area_ids"]),
                seniority["shift_duration"],
                seniority["id"]
            ))

        conn.commit()
        conn.close()

    except Exception as e:
        print("update_all_seniorities fonksiyonunda hata:", e)
        raise

def delete_seniority(seniority_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM seniority WHERE id = ?", (seniority_id,))
    conn.commit()
    conn.close()


def get_shift_areas():
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT id, area_name, min_doctors_per_area FROM shift_areas")
    rows = cur.fetchall()
    conn.close()

    return {
        row["area_name"]: {
            "id": row["id"],
            "min_doctors_per_area": row["min_doctors_per_area"]
        }
        for row in rows
    }

def add_shift_area(data):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO shift_areas (area_name, min_doctors_per_area) VALUES (?, ?)",
        (data["area_name"], data["min_doctors_per_area"])
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return new_id

def update_all_shift_areas(data):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        for area in data:
            cur.execute(
                "UPDATE shift_areas SET area_name = ?, min_doctors_per_area = ? WHERE id = ?",
                (area["area_name"], area["min_doctors_per_area"], area["id"])
            )

        conn.commit()
        conn.close()

    except Exception as e:
        print("update_all_shift_areas fonksiyonunda hata:", e)
        raise

def delete_shift_area(area_id):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM shift_areas WHERE id = ?", (area_id,))
    conn.commit()
    conn.close()


def get_schedule_data_by_id(schedule_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, schedule_data_name, schedule_data, first_day, days_in_month 
            FROM schedule_data 
            WHERE id = ?
        """, (schedule_id,))
        
        row = cur.fetchone()
        conn.close()

        return {
            "id": row["id"],
            "name": row["schedule_data_name"],
            "data": json.loads(row["schedule_data"]),
            "first_day": row["first_day"],
            "days_in_month": row["days_in_month"]
        } if row else {}

    except Exception as e:
        print("get_schedule_data_by_id fonksiyonunda hata:", e)
        return {}

def get_all_schedule_data():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("SELECT id, schedule_data_name, schedule_data, created_at FROM schedule_data ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": row["id"],
                "name": row["schedule_data_name"],
                "data": json.loads(row["schedule_data"]),
                "created_at": row["created_at"]
            }
            for row in rows
        ]

    except Exception as e:
        print("get_schedule_data fonksiyonunda hata:", e)
        return []

def add_schedule_data(name, schedule_json, first_day, days_in_month):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO schedule_data (schedule_data_name, schedule_data, first_day, days_in_month) 
            VALUES (?, ?, ?, ?)
            """,
            (name, json.dumps(schedule_json), first_day, days_in_month)
        )
        
        conn.commit()
        schedule_id = cur.lastrowid
        conn.close()

        return {"message": "Nöbet listesi başarıyla kaydedildi.", "id": schedule_id}

    except Exception as e:
        print("add_schedule_data fonksiyonunda hata:", e)
        return {"error": str(e)}

def delete_schedule_data(schedule_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("DELETE FROM schedule_data WHERE id = ?", (schedule_id,))
        conn.commit()
        conn.close()

        return {"message": "Nöbet listesi başarıyla silindi."}

    except Exception as e:
        print("delete_schedule_data fonksiyonunda hata:", e)
        return {"error": "Silme işlemi sırasında bir hata oluştu."}

def update_schedule_data(schedule_id, new_name, new_schedule_json):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute(
            "UPDATE schedule_data SET schedule_data_name = ?, schedule_data = ? WHERE id = ?",
            (new_name, json.dumps(new_schedule_json), schedule_id)
        )
        
        conn.commit()
        conn.close()

        return {"message": "Nöbet listesi başarıyla güncellendi."}

    except Exception as e:
        print("update_schedule_data fonksiyonunda hata:", e)
        return {"error": "Güncelleme işlemi sırasında bir hata oluştu."}


def get_schedule_by_id(schedule_id):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, schedule_data_id, schedule, fitness_score, log_messages, created_at 
        FROM schedules 
        WHERE id = ?
    """, (schedule_id,))

    row = cur.fetchone()
    conn.close()

    return {
        "id": row["id"],
        "schedule_data_id": row["schedule_data_id"],
        "schedule": json.loads(row["schedule"]),
        "fitness_score": row["fitness_score"],
        "log_messages": json.loads(row["log_messages"]) if row["log_messages"] else [],
        "created_at": row["created_at"]
    } if row else None

def add_schedule(schedule_data_id, schedule):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO schedules (schedule_data_id, schedule)
            VALUES (?, ?)
        """, (schedule_data_id, json.dumps(schedule)))

        conn.commit()
        schedule_id = cur.lastrowid
        conn.close()

        return schedule_id

    except Exception as e:
        print("add_schedule fonksiyonunda hata:", e)
        return None

def add_fitness_score(schedule_id, fitness_score):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("""
            UPDATE schedules
            SET fitness_score = ?
            WHERE id = ?
        """, (fitness_score, schedule_id))

        conn.commit()
        conn.close()

    except Exception as e:
        print("add_fitness_score fonksiyonunda hata:", e)

def add_log_messages(schedule_id, log_messages):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("SELECT log_messages FROM schedules WHERE id = ?", (schedule_id,))
        result = cur.fetchone()

        existing_logs = json.loads(result["log_messages"]) if result and result["log_messages"] else []
        updated_logs = existing_logs + log_messages

        cur.execute("""
            UPDATE schedules
            SET log_messages = ?
            WHERE id = ?
        """, (json.dumps(updated_logs), schedule_id))

        conn.commit()
        conn.close()

    except Exception as e:
        print("add_log_messages fonksiyonunda hata:", e)

def delete_schedule(schedule_id):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM schedules WHERE id = ?", (schedule_id,))
    conn.commit()
    conn.close()

def get_all_schedules():
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.id, s.schedule_data_id, sd.schedule_data_name, s.fitness_score
        FROM schedules s
        JOIN schedule_data sd ON s.schedule_data_id = sd.id
        ORDER BY s.created_at DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "schedule_data_id": row["schedule_data_id"],
            "schedule_data_name": row["schedule_data_name"],
            "fitness_score": row["fitness_score"]
        }
        for row in rows
    ]
