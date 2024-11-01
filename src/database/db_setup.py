# src/database/db_setup.py
import os
import sqlite3
import sys
from src.config import DATABASE_PATH

# Tambahkan path folder `src` ke dalam sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(src_path)

def create_logs_table():
    """Membuat tabel logs khusus untuk mencatat riwayat serangan."""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                attack_type TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                destination_ip TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        connection.commit()
        print("Tabel logs untuk riwayat serangan berhasil dibuat.")
    except sqlite3.Error as e:
        print(f"Error saat membuat tabel logs: {e}")
    finally:
        connection.close()

# Jalankan fungsi ini untuk setup tabel
if __name__ == "__main__":
    create_logs_table()
