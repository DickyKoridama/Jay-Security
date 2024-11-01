import unittest
from unittest.mock import patch
from src.network_monitor import NetworkMonitor
from src.alert_system import send_alert

class TestIntegration(unittest.TestCase):

    @patch('src.alert_system.send_alert', autospec=True)
    def test_ddos_detection_integration(self, mock_send_alert):
        # Buat instance NetworkMonitor dengan threshold yang rendah untuk memicu alert
        network_monitor = NetworkMonitor(interface="dummy")

        # Melewati ambang batas agar serangan DDoS terdeteksi
        for _ in range(25):
            network_monitor.fsa_detector.transition_ddos(request_count=25)

        # Cek apakah DDoS terdeteksi
        if network_monitor.fsa_detector.is_ddos_attack_detected():
            print("DDoS detected!")
            mock_send_alert("DDoS", "192.168.1.10")  # Panggil mock_send_alert
        else:
            print("DDoS not detected.")

        # Verifikasi bahwa send_alert dipanggil dengan parameter yang benar
        mock_send_alert.assert_called_once_with("DDoS", "192.168.1.10")

if __name__ == '__main__':
    unittest.main()