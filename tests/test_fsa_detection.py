import unittest
from src.fsa_detection import MultiAttackFSA

class TestMultiAttackFSA(unittest.TestCase):

    def setUp(self):
        # Inisialisasi objek MultiAttackFSA sebelum setiap pengujian
        self.normal_ips = ["192.168.1.1", "192.168.1.2"]
        self.fsa = MultiAttackFSA(normal_threshold=100, warning_threshold=200, port_scan_threshold=10, normal_ips=self.normal_ips)

    def test_sql_injection_detection(self):
        # Uji deteksi SQL Injection
        self.fsa.transition_sql("'")
        self.fsa.transition_sql("-")
        self.assertTrue(self.fsa.is_sql_attack_detected(), "SQL Injection attack should be detected.")

    def test_ddos_detection(self):
        # Uji deteksi DDoS
        self.fsa.transition_ddos(50)  # Di bawah ambang batas
        self.assertEqual(self.fsa.ddos_state, 'S0', "DDoS state should be S0.")
        
        self.fsa.transition_ddos(60)  # Melebihi ambang batas normal
        self.assertEqual(self.fsa.ddos_state, 'S1', "DDoS state should be S1.")
        
        self.fsa.transition_ddos(100)  # Melebihi ambang batas peringatan
        self.assertEqual(self.fsa.ddos_state, 'S2', "DDoS state should be S2.")

    def test_port_scan_detection(self):
        # Uji deteksi pemindaian port
        self.fsa.transition_port_scan("192.168.1.3", 5)  # IP tidak normal
        self.assertEqual(self.fsa.port_scan_state, 'S0', "Port scan state should be S0.")
        
        self.fsa.transition_port_scan("192.168.1.3", 6)  # Melebihi ambang batas pemindaian
        self.assertEqual(self.fsa.port_scan_state, 'S1', "Port scan state should be S1.")
        
        # Sekarang lakukan pemindaian yang cukup untuk mengatur kembali ke S0
        self.fsa.transition_port_scan("192.168.1.3", 5)  # Total 11, masih di S1
        self.assertEqual(self.fsa.port_scan_state, 'S1', "Port scan state should still be S1.")
        
        # Lakukan pemindaian yang cukup untuk mengatur kembali ke S0
        self.fsa.transition_port_scan("192.168.1.3", -11)  # Reset hitungan
        self.assertEqual(self.fsa.port_scan_state, 'S0', "Port scan state should be S0 after reset.")
if __name__ == '__main__':
    unittest.main()