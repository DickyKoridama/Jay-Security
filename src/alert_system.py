from twilio.rest import Client
from plyer import notification  # Import plyer untuk notifikasi desktop
from src.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, ADMIN_PHONE_NUMBER
from src.utils.alert_utils import format_alert_message

def send_notification(alert_type, src_ip):
    """Fungsi untuk menampilkan notifikasi saat serangan terdeteksi."""
    notification.notify(
        title=f'Alert: {alert_type} Detected',
        message=f'{alert_type} detected from {src_ip}',
        app_name='Alert System',
        timeout=10  # Notifikasi akan hilang setelah 10 detik
    )

def send_alert(alert_type, src_ip):
    """
    Mengirim notifikasi melalui WhatsApp menggunakan Twilio.

    Parameters:
        alert_type (str): Jenis serangan yang terdeteksi.
        src_ip (str): Alamat IP sumber serangan.
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message_body = format_alert_message(alert_type, src_ip)
    
    try:
        message = client.messages.create(
            body=message_body,
            from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
            to=f"whatsapp:{ADMIN_PHONE_NUMBER}"
        )
        print(f"Notifikasi terkirim: {message.sid}")

        # Kirim notifikasi desktop
        send_notification(alert_type, src_ip)  # Panggil fungsi notifikasi
    except Exception as e:
        print(f"Gagal mengirim notifikasi: {e}")