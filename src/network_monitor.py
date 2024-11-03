# network_monitor.py
from scapy.all import sniff, IP
import threading
from queue import Queue, Empty
import time
from src.log_handler import LogHandler
from src.fsa_detection import MultiAttackFSA
from src.alert_system import send_alert

class NetworkMonitor:
    def __init__(self, interface):
        self.interface = interface
        self.running = False
        self.packet_queue = Queue(maxsize=1000)
        
        # Daftar IP normal
        normal_ips = []
        self.fsa_detector = MultiAttackFSA(
            normal_threshold=100, 
            warning_threshold=200, 
            port_scan_threshold=10, 
            normal_ips=normal_ips
        )
        
        self.logger = LogHandler()  
        self.ddos_request_count = 0  
        self.port_scan_count = 0  

    def start_monitoring(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._sniff_packets)
            self.thread.start()

    def stop_monitoring(self):
        self.running = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join(timeout=5)

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
                "protocol": packet[IP].proto,
                "payload": packet.payload if hasattr(packet, 'payload') else None,
                "info": ""
            }
            if not self.packet_queue.full():
                self.packet_queue.put(packet_info)

            # Deteksi serangan
            attack_type = None
            if self.fsa_detector.is_ddos_attack_detected():
                attack_type = "DDoS"
            elif self.port_scan_count > self.fsa_detector.port_scan_threshold:
                attack_type = "Port Scanning"

            if attack_type:
                packet_info["alert"] = attack_type
                self.logger.log_attack(attack_type, packet_info["src_ip"], packet_info["dest_ip"])
                send_alert(attack_type, packet_info["src_ip"])
                if not self.packet_queue.full():
                    self.packet_queue.put(packet_info)

            # Reset counter sesuai deteksi
            if not self.fsa_detector.is_ddos_attack_detected():
                self.ddos_request_count = 0
            if not self.fsa_detector.is_port_scan_detected():
                self.port_scan_count = 0

    def get_packet(self):
        try:
            return self.packet_queue.get_nowait()
        except Empty:
            return None
