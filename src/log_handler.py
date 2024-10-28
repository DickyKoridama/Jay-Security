# src/log_handler.py
import logging
from src.config import LOG_FILE_PATH  # Updated import path

class LogHandler:
    """Class untuk mengelola logging aplikasi."""

    def __init__(self):
        # Konfigurasi logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(LOG_FILE_PATH),
                logging.StreamHandler()
            ]
        )

    def log_activity(self, message):
        """Log aktivitas informasi."""
        logging.info(message)

    def log_warning(self, message):
        """Log aktivitas warning."""
        logging.warning(message)

    def log_error(self, message):
        """Log aktivitas error."""
        logging.error(message)

    def close_connection(self):
        """Tutup semua handler jika diperlukan (opsional)."""
        for handler in logging.root.handlers[:]:
            handler.close()
            logging.root.removeHandler(handler)
