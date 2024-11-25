import unittest
from unittest.mock import patch, MagicMock
from src.alert_system import send_alert, send_notification

class TestAlertSystem(unittest.TestCase):

    @patch("src.alert_system.Client")
    def test_send_alert_success(self, mock_client):
        """Test apakah notifikasi WhatsApp berhasil dikirim."""
        mock_instance = mock_client.return_value
        mock_instance.messages.create.return_value.sid = "SMXXXXXXXXXXXXXXXXXXX"

        send_alert("DDoS", "192.168.0.1")

        # Pastikan Twilio dipanggil dengan parameter yang benar
        mock_instance.messages.create.assert_called_once()

    @patch("src.alert_system.Client")
    def test_send_alert_twilio_failure(self, mock_client):
        """Test fallback saat Twilio gagal."""
        mock_instance = mock_client.return_value
        mock_instance.messages.create.side_effect = Exception("Twilio error")

        with patch("src.alert_system.send_notification") as mock_notification:
            send_alert("Port Scanning", "192.168.0.1")

            # Pastikan fallback notifikasi desktop dipanggil
            mock_notification.assert_called_once_with("Port Scanning", "192.168.0.1")

    @patch("src.alert_system.notification.notify")
    def test_send_notification(self, mock_notify):
        """Test apakah notifikasi desktop berhasil."""
        send_notification("SQL Injection", "192.168.0.1")

        # Pastikan notifikasi desktop dipanggil
        mock_notify.assert_called_once()

if __name__ == '__main__':
    unittest.main()
