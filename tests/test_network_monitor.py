# tests/test_network_monitor.py
import unittest
from queue import Queue
from src.network_monitor import NetworkMonitor
from scapy.layers.inet import IP  # Mengimpor IP dari Scapy untuk digunakan di MockPacket

# MockPacket yang kompatibel dengan NetworkMonitor
class MockPacket(dict):
    def __init__(self, src_ip, dst_ip, proto):
        self[IP] = type('IPLayer', (object,), {"src": src_ip, "dst": dst_ip, "proto": proto})

class TestNetworkMonitor(unittest.TestCase):

    def setUp(self):
        # Buat instance NetworkMonitor dengan interface dummy
        self.network_monitor = NetworkMonitor(interface="dummy")
        self.network_monitor.packet_queue = Queue(maxsize=100)  # Queue untuk antrean paket

    def test_packet_queueing(self):
        # Simulasi paket dan tambahkan ke queue
        packet = {"src_ip": "192.168.1.10", "dest_ip": "192.168.1.1", "protocol": 6}
        self.network_monitor.packet_queue.put(packet)
        queued_packet = self.network_monitor.get_packet()
        self.assertEqual(queued_packet, packet, "Packet tidak sesuai dengan yang diantrekan.")

    def test_process_packet(self):
        # Proses paket mock dan periksa apakah paket masuk ke queue
        packet = {"src_ip": "192.168.1.10", "dest_ip": "192.168.1.1", "protocol": 6}
        self.network_monitor._process_packet(MockPacket(src_ip=packet["src_ip"], dst_ip=packet["dest_ip"], proto=packet["protocol"]))
        self.assertFalse(self.network_monitor.packet_queue.empty(), "Packet tidak diproses dengan benar.")

if __name__ == '__main__':
    unittest.main()
