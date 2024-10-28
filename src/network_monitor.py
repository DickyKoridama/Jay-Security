from scapy.all import sniff, IP
import threading
from queue import Queue
import time

class NetworkMonitor:
    def __init__(self, interface):
        self.interface = interface
        self.running = False
        self.packet_queue = Queue(maxsize=1000)  # Batasi ukuran queue

    def start_monitoring(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._sniff_packets)
            self.thread.start()

    def stop_monitoring(self):
        self.running = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join(timeout=5)  # Tunggu maksimal 5 detik

    def _sniff_packets(self):
        try:
            sniff(iface=self.interface, prn=self._process_packet, store=False, 
                  stop_filter=lambda x: not self.running)
        except Exception as e:
            print(f"Error in sniffing: {e}")

    def _process_packet(self, packet):
        if IP in packet:
            packet_info = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "src_ip": packet[IP].src,
                "dest_ip": packet[IP].dst,
                "protocol": packet[IP].proto
            }
            if not self.packet_queue.full():
                self.packet_queue.put(packet_info)

    def get_packet(self):
        try:
            return self.packet_queue.get_nowait()
        except Queue.Empty:
            return None