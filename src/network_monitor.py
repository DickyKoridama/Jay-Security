import os
import sys
from scapy.all import sniff, IP
import threading
from queue import Queue, Empty
import time
from src.log_handler import LogHandler
from src.alert_system import send_alert
from src.utils.fsa_utils import initialize_fsa

class NetworkMonitor:
    def __init__(self, interface, fsa_detector):
        self.interface = interface
        self.running = False
        self.packet_queue = Queue(maxsize=1000)
        self.logger = LogHandler()
        self.detector = fsa_detector
        print(f"[INIT] NetworkMonitor initialized on interface: {interface}")

    def start_monitoring(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self._sniff_packets, daemon=True).start()
            threading.Thread(target=self._process_packet_thread, daemon=True).start()

    def stop_monitoring(self):
        self.running = False

    def _sniff_packets(self):
        try:
            sniff(iface=self.interface, filter="tcp", prn=self._enqueue_packet, store=False, stop_filter=lambda _: not self.running)
        except Exception as e:
            self.logger.log_activity(f"[ERROR] Sniffing failed: {e}")

   
    def _enqueue_packet(self, packet):
        if not packet.haslayer(IP):
            return
        src_ip = str(packet[IP].src)
        dest_ip = str(packet[IP].dst)
        dest_port = getattr(packet[IP], 'dport', None)
        payload = getattr(packet, 'payload', None)
        protocol = str(packet[IP].proto) if hasattr(packet[IP], 'proto') else "Unknown"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        packet_info = {
            "src_ip": src_ip,
            "dest_ip": dest_ip,
            "dest_port": dest_port,
            "protocol": protocol,
            "timestamp": timestamp, 
            "payload": str(payload) if payload else "",
        }
        if not self.packet_queue.full():
            self.packet_queue.put(packet_info)


    def _process_packet_thread(self):
        while self.running:
            try:
                packet_info = self.packet_queue.get(timeout=1)
                self._detect_attacks(packet_info)
            except Empty:
                continue

    def _detect_attacks(self, packet_info):
        src_ip = packet_info["src_ip"]
        dest_ip = packet_info["dest_ip"]
        dest_port = packet_info.get("dest_port")
        payload = packet_info.get("payload", "")

        if dest_port is not None and self.detector.detect_port_scan(src_ip, dest_port):
            print(f"[ALERT] Port scanning detected from {src_ip}")
            self.logger.log_attack("Port Scanning", src_ip, dest_ip) 
            send_alert("Port Scanning", src_ip)
            self.detector.reset_port_scan(src_ip)
            return

      
        if not self.detector.port_scan_fsa.is_attack_detected(src_ip):
            if self.detector.detect_ddos():
                print(f"[ALERT] DDoS detected from {src_ip}")
                self.logger.log_attack("DDoS", src_ip, dest_ip) 
                send_alert("DDoS", src_ip)
                self.detector.reset_ddos()

        
        if payload and self.detector.detect_sql_injection(payload):
            print(f"[ALERT] SQL Injection detected from {src_ip}")
            self.logger.log_attack("SQL Injection", src_ip, dest_ip)  
            send_alert("SQL Injection", src_ip)
            self.detector.reset_sql_injection()

    def get_packet(self):
        """Retrieve packet from queue."""
        try:
            return self.packet_queue.get_nowait()
        except Empty:
            return None
