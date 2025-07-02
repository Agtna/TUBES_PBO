import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def insert_laporan(data: dict):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO laporan (nama, deskripsi, tipe, latitude, longitude, tanggal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data['nama'], data['deskripsi'], data['tipe'],
            data['latitude'], data['longitude'], data['tanggal']
        ))
        conn.commit()

def get_all_laporan():
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM laporan ORDER BY tanggal DESC", conn)
def delete_laporan_by_id(id_laporan: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM laporan WHERE id = ?", (id_laporan,))
            conn.commit()
        return True
    except:
        return False
