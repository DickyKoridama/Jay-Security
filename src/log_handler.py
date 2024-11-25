import sqlite3
import os
from src.config import DATABASE_PATH

class LogHandler:
    """Class untuk mengelola pencatatan log aktivitas dan riwayat serangan di aplikasi."""

    def __init__(self):
        # Buat direktori database jika belum ada
        db_dir = os.path.dirname(DATABASE_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

       
        self._initialize_database()

    def _initialize_database(self):
        """Inisialisasi database dan tabel jika belum ada."""
        conn, cursor = self._get_connection()
        try:
            # Tabel untuk log aktivitas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    level TEXT,
                    message TEXT
                )
            """)

            # Tabel untuk riwayat serangan
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attack_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    attack_type TEXT,
                    source_ip TEXT,
                    destination_ip TEXT,
                    status TEXT
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal membuat tabel database: {e}")
        finally:
            conn.close()

    def _get_connection(self):
        """Membuka koneksi SQLite baru."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        return conn, cursor

    def log_activity(self, message, level="info"):
        """
        Mencatat pesan log aktivitas ke tabel logs.
        Parameters:
            message (str): Pesan log aktivitas.
            level (str): Level log, default "info".
        """
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""
                INSERT INTO logs (level, message)
                VALUES (?, ?)
            """, (level.upper(), message))
            conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal mencatat aktivitas log ke database: {e}")
        finally:
            conn.close()
        
        print(f"[{level.upper()}] {message}")

    def log(self, message, level="info"):
        """Alias untuk log_activity, memastikan kompatibilitas."""
        self.log_activity(message, level)

    def log_attack(self, attack_type, src_ip, dest_ip=None, status="Not Mitigated"):
        """
        Mencatat riwayat serangan ke tabel attack_logs.
        Parameters:
            attack_type (str): Jenis serangan.
            src_ip (str): IP sumber serangan.
            dest_ip (str): IP tujuan serangan, default "Unknown".
            status (str): Status mitigasi serangan, default "Not Mitigated".
        """
        dest_ip = dest_ip or "Unknown" 
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""
                INSERT INTO attack_logs (attack_type, source_ip, destination_ip, status)
                VALUES (?, ?, ?, ?)
            """, (attack_type, src_ip, dest_ip, status))
            conn.commit()
        except sqlite3.Error as e:
            self.log_activity(f"Gagal mencatat serangan ke database: {e}", level="error")
        finally:
            conn.close()


    def migrate_logs_table(self):
        """
        Memperbarui tabel logs di database untuk menambahkan kolom level jika belum ada.
        """
        conn, cursor = None, None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

          
            cursor.execute("PRAGMA table_info(logs);")
            columns = [col[1] for col in cursor.fetchall()]
            if "level" not in columns:
                
                cursor.execute("ALTER TABLE logs ADD COLUMN level TEXT DEFAULT 'INFO'")
                conn.commit()
                print("[INFO] Kolom 'level' berhasil ditambahkan ke tabel logs.")
            else:
                print("[INFO] Tabel logs sudah memiliki kolom 'level'.")
        except sqlite3.Error as e:
                        print(f"[ERROR] Gagal memperbarui tabel logs: {e}")
        finally:
            if conn:
                conn.close()


log_handler = LogHandler()
log_handler.migrate_logs_table()