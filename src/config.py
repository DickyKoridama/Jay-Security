# src/config.py
import os
import yaml

# Menentukan path absolut ke config.yml di direktori root proyek
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.join(root_dir, "config.yml")

# Memuat konfigurasi dari file config.yml
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# Twilio API Configuration
TWILIO_ACCOUNT_SID = config["twilio"]["account_sid"]
TWILIO_AUTH_TOKEN = config["twilio"]["auth_token"]
TWILIO_PHONE_NUMBER = config["twilio"]["phone_number"]
ADMIN_PHONE_NUMBER = config["twilio"]["admin_phone_number"]

# Database Configuration
DATABASE_PATH = config["database"]["path"]

# Logging Configuration
LOG_FILE_PATH = config["logging"]["file_path"]

# Attack Detection Threshold Level
DETECTION_THRESHOLD_LEVEL = config["detection"]["threshold_level"]
