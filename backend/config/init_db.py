import sqlite3
import os
import sys

# Paketlenmiş uygulama için veritabanı yolunu belirle
def get_db_path():
    # PyInstaller ile paketlenmiş mi kontrol et
    if getattr(sys, 'frozen', False):
        # Paketlenmiş uygulama için
        if os.path.exists(os.path.join(os.path.dirname(sys.executable), "mydata.db")):
            # Exe ile aynı dizinde
            return os.path.join(os.path.dirname(sys.executable), "mydata.db")
        elif os.path.exists(os.path.join(os.path.dirname(os.path.dirname(sys.executable)), "resources", "mydata.db")):
            # Electron resources klasöründe
            return os.path.join(os.path.dirname(os.path.dirname(sys.executable)), "resources", "mydata.db")
        else:
            # Varsayılan konum
            return os.path.join(os.path.dirname(sys.executable), "mydata.db")
    else:
        # Geliştirme ortamında
        return os.path.join(os.path.dirname(__file__), "..", "mydata.db")

DB_PATH = get_db_path()

def init_db():
    # Veritabanı dosyasının var olup olmadığını kontrol et
    if os.path.exists(DB_PATH):
        print(f"Veritabanı dosyası bulundu: {DB_PATH}")
        # Veritabanı bağlantısını test et
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cur.fetchall()
            print(f"Mevcut tablolar: {[table[0] for table in tables]}")
            conn.close()
            return  # Mevcut veritabanı kullanılıyor, başka bir işlem yapma
        except Exception as e:
            print(f"Veritabanı bağlantı hatası: {e}")
    else:
        print(f"Veritabanı dosyası bulunamadı: {DB_PATH}")
        print("Yeni bir veritabanı oluşturuluyor...")

        # Yeni veritabanı oluştur
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Kullanıcılar tablosunu oluştur
        cur.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)

        # Gazi-Acil kullanıcısını ekle
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        password_hash = bcrypt.generate_password_hash("gazi1234").decode('utf-8')
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("Gazi-Acil", password_hash))
        print("Gazi-Acil kullanıcısı oluşturuldu")

        # Diğer tabloları oluştur
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
