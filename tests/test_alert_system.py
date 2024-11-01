import unittest
from unittest.mock import patch, MagicMock
from src.alert_system import send_alert, send_notification
from src.config import TWILIO_PHONE_NUMBER, ADMIN_PHONE_NUMBER  # type: ignore

class TestAlertSystem(unittest.TestCase):

    @patch('src.alert_system.Client')
    @patch('src.alert_system.format_alert_message')
    @patch('src.config.TWILIO_PHONE_NUMBER', new="+14155238886")
    @patch('src.config.ADMIN_PHONE_NUMBER', new="+6282199118088")
    @patch('src.config.TWILIO_ACCOUNT_SID', new='mock_account_sid')
    @patch('src.config.TWILIO_AUTH_TOKEN', new='mock_auth_token')
    @patch('src.alert_system.notification.notify')  # Mock notifikasi
    def test_send_alert(self, mock_notify, mock_format_alert_message, mock_client):
        # Siapkan data untuk pengujian
        alert_type = "DDoS"
        src_ip = "192.168.1.10"
        mock_format_alert_message.return_value = "Alert: DDoS detected from 192.168.1.10"
        
        # Buat instance mock untuk client dan metode create
        mock_message = MagicMock()
        mock_message.sid = "SM3b90a8b3d1d6dbde4afcd122d03120bc"
        mock_client.return_value.messages.create.return_value = mock_message

        # Panggil fungsi yang ingin diuji
        send_alert(alert_type, src_ip)

        # Verifikasi bahwa format_alert_message dipanggil dengan argumen yang benar
        mock_format_alert_message.assert_called_once_with(alert_type, src_ip)

        # Verifikasi bahwa client.messages.create dipanggil dengan argumen yang benar
        mock_client.return_value.messages.create.assert_called_once_with(
            body="Alert: DDoS detected from 192.168.1.10",
            from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
            to=f"whatsapp:{ADMIN_PHONE_NUMBER}"
        )

        # Verifikasi bahwa notifikasi dipanggil dengan argumen yang benar
        mock_notify.assert_called_once_with(
            title='Alert: DDoS Detected',
            message='DDoS detected from 192.168.1.10',
            app_name='Alert System',
            timeout=10
        )

if __name__ == '__main__':
    unittest.main()