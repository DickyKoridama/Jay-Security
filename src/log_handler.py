# src/log_handler.py
import sqlite3
import os
from src.config import DATABASE_PATH

class LogHandler:
    """Class untuk mengelola pencatatan serangan di database."""

    def __init__(self):
        # Buat direktori database jika belum ada
        db_dir = os.path.dirname(DATABASE_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def _get_connection(self):
        """Membuka koneksi SQLite baru."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        return conn, cursor

    def log_attack(self, attack_type, src_ip, dest_ip, status="Not Mitigated"):
        """Mencatat riwayat serangan ke database."""
        conn, cursor = self._get_connection()
        try:
            cursor.execute(
                '''
                INSERT INTO logs (timestamp, attack_type, source_ip, destination_ip, status)
                VALUES (datetime('now'), ?, ?, ?, ?)
                ''',
                (attack_type, src_ip, dest_ip, status)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Gagal mencatat serangan ke database: {e}")
        finally:
            conn.close()

    def close(self):
        """Menutup semua handler di logger (tidak diperlukan handler tambahan)."""
        pass
