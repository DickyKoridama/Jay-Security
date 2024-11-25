import os
import yaml

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.join(root_dir, "config.yml")


try:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"File konfigurasi tidak ditemukan di path: {config_path}")
except yaml.YAMLError as e:
    raise ValueError(f"Kesalahan dalam parsing file YAML: {e}")


TWILIO_ACCOUNT_SID = config.get("twilio", {}).get("account_sid", "")
TWILIO_AUTH_TOKEN = config.get("twilio", {}).get("auth_token", "")
TWILIO_PHONE_NUMBER = config.get("twilio", {}).get("phone_number", "")
ADMIN_PHONE_NUMBER = config.get("twilio", {}).get("admin_phone_number", "")


DATABASE_PATH = config.get("database", {}).get("path", "database/jaysecurity.db")


LOG_FILE_PATH = config.get("logging", {}).get("file_path", "logs/jaysecurity.log")


DETECTION_THRESHOLD_LEVEL = config.get("detection", {}).get("threshold_level", "medium")


if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
    raise ValueError("Konfigurasi Twilio tidak lengkap. Periksa 'account_sid' dan 'auth_token' di config.yml.")
if not TWILIO_PHONE_NUMBER or not ADMIN_PHONE_NUMBER:
    print("[WARNING] Nomor telepon Twilio atau admin tidak disediakan. Notifikasi WhatsApp mungkin gagal.")
