import unittest
from src.fsa_detection import MultiAttackFSA

class TestMultiAttackFSA(unittest.TestCase):
    def setUp(self):
        """
        Setup objek FSA untuk digunakan dalam semua test case.
        """
        self.fsa = MultiAttackFSA(
            normal_threshold=100,
            warning_threshold=200,
            port_scan_threshold=10,
            normal_ips=["192.168.1.1"]
        )

    def test_sql_injection_detection(self):
        """
        Menguji deteksi SQL Injection.
        """
        sql_input = "SELECT * FROM users WHERE username='admin'--"
        for char in sql_input:
            self.fsa.transition_sql(char)
        self.assertTrue(self.fsa.is_sql_attack_detected(), "SQL Injection tidak terdeteksi padahal harusnya terdeteksi.")

        # Reset dan uji input normal
        self.fsa.sql_state = 'S0'
        normal_input = "SELECT * FROM users WHERE username='admin'"
        for char in normal_input:
            self.fsa.transition_sql(char)
        self.assertFalse(self.fsa.is_sql_attack_detected(), "SQL Injection terdeteksi padahal tidak ada serangan.")

    def test_ddos_detection(self):
        """
        Menguji deteksi serangan DDoS.
        """
        # Uji transisi ke S1
        for _ in range(101):  # Melebihi normal_threshold (100)
            self.fsa.transition_ddos(1)
        self.assertEqual(self.fsa.ddos_state, 'S1', "FSA tidak masuk state S1 setelah melebihi ambang batas normal.")

        # Uji transisi ke S2
        for _ in range(100):  # Melebihi warning_threshold (200)
            self.fsa.transition_ddos(1)
        self.assertEqual(self.fsa.ddos_state, 'S2', "FSA tidak masuk state S2 setelah melebihi ambang batas peringatan.")
        self.assertTrue(self.fsa.is_ddos_attack_detected(), "Serangan DDoS tidak terdeteksi padahal harusnya terdeteksi.")

    def test_port_scan_detection(self):
        """
        Menguji deteksi port scanning.
        """
        ip = "10.0.0.5"

        # Tambahkan scan count hingga melebihi ambang batas
        for _ in range(15):
            self.fsa.transition_port_scan(ip, 1)
        self.assertTrue(self.fsa.is_port_scan_detected(), "Port scanning tidak terdeteksi padahal harusnya terdeteksi.")
        self.assertEqual(self.fsa.port_scan_state, 'S1', "FSA tidak masuk state S1 setelah melebihi ambang batas port scanning.")

        # Reset scan count dan uji bahwa state kembali ke S0
        for _ in range(5):
            self.fsa.transition_port_scan(ip, -1)
        self.assertFalse(self.fsa.is_port_scan_detected(), "Port scanning terdeteksi padahal harusnya tidak ada serangan.")
        self.assertEqual(self.fsa.port_scan_state, 'S0', "FSA tidak kembali ke state S0 setelah scan count turun di bawah ambang batas.")

    def test_normal_ip_exclusion(self):
        """
        Menguji bahwa IP dalam daftar normal tidak dianggap melakukan port scanning.
        """
        ip = "192.168.1.1"  # IP yang masuk dalam daftar normal
        for _ in range(15):
            self.fsa.transition_port_scan(ip, 1)
        self.assertFalse(self.fsa.is_port_scan_detected(), "Port scanning terdeteksi untuk IP yang ada dalam daftar normal.")
        
