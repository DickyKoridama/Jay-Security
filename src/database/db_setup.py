# db_setup.py
import sys
import os
import sqlite3

# Menambahkan path utama proyek ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from config import DATABASE_PATH

def create_connection():
    """Membuat koneksi ke database SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        print("Koneksi ke database berhasil.")
    except sqlite3.Error as e:
        print(f"Error dalam menghubungkan ke database: {e}")
    return conn

def setup_database():
    """Menyiapkan tabel untuk menyimpan log jika belum ada."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Membuat tabel logs jika belum ada
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
            conn.commit()
            print("Tabel logs telah siap.")
        except sqlite3.Error as e:
            print(f"Error saat membuat tabel: {e}")
        finally:
            conn.close()
    else:
        print("Koneksi ke database gagal.")

if __name__ == "__main__":
    setup_database()
