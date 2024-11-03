# src/fsa_detection.py
class MultiAttackFSA:  
    def __init__(self, normal_threshold, warning_threshold, port_scan_threshold, normal_ips):  
        self.sql_state = 'S0'  
        self.ddos_state = 'S0'  
        self.port_scan_state = 'S0'  
        self.normal_threshold = normal_threshold  
        self.warning_threshold = warning_threshold  
        self.port_scan_threshold = port_scan_threshold  
        self.normal_ips = normal_ips
        self.scan_counts = {}
        self.ddos_request_count = 0 

    def transition_sql(self, input_char):  
        if self.sql_state == 'S0':  
            if input_char == "'":  
                self.sql_state = 'S1'  
            elif input_char == '-':  
                self.sql_state = 'S2'  
        elif self.sql_state == 'S1':  
            if input_char == '-':  
                self.sql_state = 'S3'    
        elif self.sql_state == 'S2':  
            self.sql_state = 'S0'  

    def transition_ddos(self, request_count):  
        self.ddos_request_count += request_count 
        print(f"Current DDoS state: {self.ddos_state}, Total Request count: {self.ddos_request_count}")
        
        if self.ddos_state == 'S0':  
            if self.ddos_request_count > self.normal_threshold:  
                self.ddos_state = 'S1'  
        elif self.ddos_state == 'S1':  
            if self.ddos_request_count > self.warning_threshold:  
                self.ddos_state = 'S2'  # Deteksi DDoS tercapai
            
        print(f"New DDoS state: {self.ddos_state}")

    def transition_port_scan(self, ip, scan_count):  
        if ip in self.normal_ips:
            return  
        
        if ip not in self.scan_counts:
            self.scan_counts[ip] = 0
                
        self.scan_counts[ip] += scan_count  
        
        if self.port_scan_state == 'S0':  
            if self.scan_counts[ip] > self.port_scan_threshold:  
                self.port_scan_state = 'S1'  # Deteksi port scanning tercapai
        elif self.port_scan_state == 'S1':  
            if self.scan_counts[ip] <= self.port_scan_threshold:  
                self.port_scan_state = 'S0'  # Kembali ke kondisi normal
                self.scan_counts[ip] = 0  

    def is_sql_attack_detected(self):  
        return self.sql_state == 'S3'  

    def is_ddos_attack_detected(self):  
        return self.ddos_state == 'S2'  # Tidak memerlukan argumen tambahan

    def is_port_scan_detected(self):  
        return self.port_scan_state == 'S1'
