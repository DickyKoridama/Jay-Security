import ipaddress
from collections import deque, defaultdict
import time

class SQLInjectionFSA:
    def __init__(self, keywords=None):
        self.state = 'S0'
        self.transitions = {
            'S0': {"'": 'S1', '-': 'S2', "SELECT": 'S3', "/*": 'S4'},
            'S1': {"--": 'S5', ";": 'S5', "*/": 'S0'},
            'S2': {"default": 'S0'},
            'S3': {"FROM": 'S6', ";": 'S5'},
            'S4': {"*/": 'S0'},
            'S5': {"default": 'S5'},
            'S6': {"WHERE": 'S7'},
            'S7': {"'": 'S1', "AND": 'S8', "OR": 'S8'},
            'S8': {"'": 'S1', ";": 'S5'},
        }
        self.keywords = keywords or {"SELECT", "FROM", "WHERE", "AND", "OR", "DROP", "INSERT", "DELETE", "/*", "*/", "--", ";"}

    def transition(self, input_token):
        token = input_token.upper() if isinstance(input_token, str) else input_token
        next_state = self.transitions.get(self.state, {}).get(token, self.transitions.get(self.state, {}).get("default", 'S0'))
        print(f"[TRANSITION] SQLInjectionFSA: {self.state} -> {next_state} on token '{token}'")
        self.state = next_state

    def is_attack_detected(self):
        return self.state in {'S5'}

    def reset(self):
        self.state = 'S0'
        print("[RESET] SQLInjectionFSA reset to initial state.")

class DDoSFSA:
    def __init__(self, normal_threshold, warning_threshold, burst_threshold, time_window=30):
        self.state = 'S0'
        self.requests = deque()
        self.time_window = time_window
        self.normal_threshold = normal_threshold
        self.warning_threshold = warning_threshold
        self.burst_threshold = burst_threshold

    def transition(self):
        current_time = time.time()
        self.requests.append(current_time)

        while self.requests and self.requests[0] < current_time - self.time_window:
            self.requests.popleft()

        request_count = len(self.requests)
        burst_rate = request_count / self.time_window

        if self.state == 'S0' and burst_rate > self.burst_threshold:
            self.state = 'S1'
        elif self.state == 'S1' and request_count > self.normal_threshold:
            self.state = 'S2'
        elif self.state == 'S2' and request_count > self.warning_threshold:
            self.state = 'S3'

        print(f"[TRANSITION] DDoSFSA state: {self.state} with request count: {request_count} and burst rate: {burst_rate:.2f}")

    def is_attack_detected(self):
        return self.state == 'S3'

    def reset(self):
        self.state = 'S0'
        self.requests.clear()
        print("[RESET] DDoSFSA reset to initial state.")

class PortScanFSA:
    def __init__(self, threshold, time_window=30, white_list=None):
        self.state = 'S0'
        self.port_access = defaultdict(lambda: deque())
        self.time_window = time_window
        self.threshold = threshold
        self.white_list = white_list or []

    def transition(self, ip, port):
        if ip in self.white_list:
            print(f"[INFO] IP {ip} in whitelist, ignoring.")
            return

        current_time = time.time()
        self.port_access[ip].append((port, current_time))

        while self.port_access[ip] and self.port_access[ip][0][1] < current_time - self.time_window:
            self.port_access[ip].popleft()

        accessed_ports = {entry[0] for entry in self.port_access[ip]}
        print(f"[DEBUG] PortScanFSA: IP={ip}, Ports Accessed={len(accessed_ports)}, Threshold={self.threshold}")

        if len(accessed_ports) > self.threshold:
            self.state = 'S1'
            print(f"[ALERT] Port scanning detected for IP {ip}.")
        else:
            self.state = 'S0'

    def is_attack_detected(self, ip):
        return self.state == 'S1'

    def reset(self, ip):
        print(f"[RESET] PortScanFSA reset for IP {ip}.")
        self.port_access[ip].clear()



class MultiAttackDetector:
    def __init__(self, ddos_config, port_scan_config, sql_config):
        self.ddos_fsa = DDoSFSA(**ddos_config)
        self.port_scan_fsa = PortScanFSA(**port_scan_config)
        self.sql_fsa = SQLInjectionFSA(**sql_config)

    def detect_ddos(self):
        self.ddos_fsa.transition()
        return self.ddos_fsa.is_attack_detected()

    def detect_port_scan(self, ip, port):
        self.port_scan_fsa.transition(ip, port)
        return self.port_scan_fsa.is_attack_detected(ip)

    def detect_sql_injection(self, payload):
        for token in payload.split():
            self.sql_fsa.transition(token)
        return self.sql_fsa.is_attack_detected()

    def reset_ddos(self):
        self.ddos_fsa.reset()

    def reset_port_scan(self, ip):
        self.port_scan_fsa.reset(ip)

    def reset_sql_injection(self):
        self.sql_fsa.reset()
