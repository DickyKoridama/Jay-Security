# src/fsa_detection.py

class FSADetector:
    def __init__(self):
        self.state = 'initial'  # State awal

    def process_packet(self, packet):
        # Logika untuk memproses paket dan mengubah state
        if self.state == 'initial':
            # Cek kondisi untuk transisi ke state berikutnya
            if self.check_for_attack(packet):
                self.state = 'attack_detected'
                return True  # Serangan terdeteksi
        elif self.state == 'attack_detected':
            # Logika untuk menangani serangan yang terdeteksi
            pass
        return False  # Tidak ada serangan yang terdeteksi

    def check_for_attack(self, packet):
        # Logika untuk memeriksa apakah paket sesuai dengan pola serangan
        # Misalnya, jika paket memiliki src_ip tertentu atau protokol tertentu
        if packet['src_ip'] == '192.168.1.100':  # Contoh IP penyerang
            return True
        return False