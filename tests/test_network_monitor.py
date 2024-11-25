import unittest
from unittest.mock import patch, MagicMock
from scapy.all import IP, Ether, Raw
from src.network_monitor import NetworkMonitor


class TestNetworkMonitor(unittest.TestCase):
    def setUp(self):
        """Setup sebelum setiap pengujian."""
        self.interface = "eth0"
        self.network_monitor = NetworkMonitor(self.interface)

    @patch("src.alert_system.send_alert")
    def test_detect_attacks_ddos(self, mock_send_alert):
        """
        Test apakah deteksi DDoS berhasil.
        """
        # Buat paket jaringan nyata menggunakan Scapy
        packet = Ether() / IP(src="192.168.0.1", dst="192.168.0.2", proto=6)

        # Kirim beberapa paket untuk memicu DDoS
        for _ in range(101):  # Sesuai dengan ambang batas normal_threshold
            self.network_monitor._detect_attacks({
                "src_ip": packet[IP].src,
                "dest_ip": packet[IP].dst,
                "protocol": packet[IP].proto,
            })

        # Periksa apakah send_alert dipanggil dengan parameter yang benar
        mock_send_alert.assert_called_once_with("DDoS", "192.168.0.1")

    @patch("src.alert_system.send_alert")
    def test_detect_attacks_sql_injection(self, mock_send_alert):
        """
        Test apakah deteksi SQL Injection berhasil.
        """
        # Buat paket jaringan dengan payload mencurigakan
        payload = "' OR '1'='1"  # Pola SQL Injection
        packet = Ether() / IP(src="192.168.0.1", dst="192.168.0.2", proto=6) / Raw(load=payload)

        # Kirim paket untuk memicu deteksi SQL Injection
        self.network_monitor._detect_attacks({
            "src_ip": packet[IP].src,
            "dest_ip": packet[IP].dst,
            "protocol": packet[IP].proto,
            "payload": payload,
        })

        # Periksa apakah send_alert dipanggil dengan parameter yang benar
        mock_send_alert.assert_called_once_with("SQL Injection", "192.168.0.1")


if __name__ == "__main__":
    unittest.main()
