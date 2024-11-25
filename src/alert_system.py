from twilio.rest import Client
from plyer import notification
from src.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    ADMIN_PHONE_NUMBER,
)
from src.utils.alert_utils import format_alert_message
from src.log_handler import LogHandler
import time

logger = LogHandler()

# Menyimpan waktu terakhir pengiriman notifikasi untuk tiap jenis serangan
last_sent_time = {}

def can_send_alert(alert_type, interval=60):
    """
    Memeriksa apakah notifikasi dapat dikirim berdasarkan interval waktu tertentu.
    Parameters:
        alert_type (str): Jenis serangan (misalnya: "DDoS", "Port Scanning", "SQL Injection").
        interval (int): Jeda minimum antar notifikasi (dalam detik).
    Returns:
        bool: True jika notifikasi dapat dikirim, False jika masih dalam jeda.
    """
    global last_sent_time
    now = time.time()
    if alert_type not in last_sent_time:
        last_sent_time[alert_type] = 0  # Inisialisasi jika belum ada
    if now - last_sent_time[alert_type] > interval:
        last_sent_time[alert_type] = now
        return True
    return False

def send_notification(alert_type, src_ip):
    """
    Menampilkan notifikasi desktop untuk serangan yang terdeteksi.
    Parameters:
        alert_type (str): Jenis serangan.
        src_ip (str): Alamat IP sumber serangan.
    """
    try:
        notification.notify(
            title=f'Alert: {alert_type} Detected',
            message=f'{alert_type} detected from {src_ip}',
            app_name='Alert System',
            timeout=10,  # Durasi notifikasi desktop (dalam detik)
        )
        logger.log(f"Notifikasi desktop berhasil dikirim: {alert_type} dari {src_ip}", level="info")
    except Exception as e:
        logger.log(f"Gagal menampilkan notifikasi desktop: {e}", level="error")

def send_alert(alert_type, src_ip):
    """
    Mengirim notifikasi melalui WhatsApp dan notifikasi desktop.
    Parameters:
        alert_type (str): Jenis serangan yang terdeteksi.
        src_ip (str): Alamat IP sumber serangan.
    """
    src_ip = str(src_ip)  # Konversi IP ke string untuk konsistensi

    # Periksa apakah kita dapat mengirim notifikasi berdasarkan rate limit
    if not can_send_alert(alert_type, interval=60):
        logger.log(f"[INFO] Notifikasi {alert_type} dari {src_ip} ditunda karena rate limit.", level="info")
        return

    # Format pesan
    message_body = format_alert_message(alert_type, src_ip)

    # Kirim notifikasi desktop
    send_notification(alert_type, src_ip)

    # Kirim notifikasi WhatsApp
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
            to=f"whatsapp:{ADMIN_PHONE_NUMBER}",
        )
        logger.log(f"Notifikasi WhatsApp berhasil terkirim: {message.sid}", level="info")
    except Exception as e:
        logger.log(f"Gagal mengirim notifikasi WhatsApp: {e}", level="error")
        print("[FALLBACK] Tidak dapat mengirim notifikasi WhatsApp. Silakan periksa log.")
