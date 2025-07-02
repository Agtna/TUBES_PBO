import sqlite3
from konfigurasi import DB_PATH

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS laporan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            deskripsi TEXT,
            tipe TEXT,
            latitude REAL,
            longitude REAL,
            tanggal DATE NOT NULL
        );
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
