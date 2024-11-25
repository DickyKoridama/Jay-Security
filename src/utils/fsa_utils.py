from src.fsa_detection import MultiAttackDetector

def initialize_fsa(normal_threshold=100, warning_threshold=200, port_scan_threshold=10, burst_threshold=10, normal_ips=None):
    if normal_ips is None:
        normal_ips = ["192.168.1.1", "192.168.1.7", "192.168.56.111"]
    print(f"[INIT] FSA initialized with thresholds: normal={normal_threshold}, warning={warning_threshold}, port_scan={port_scan_threshold}, burst={burst_threshold}")
    ddos_config = {
        "normal_threshold": normal_threshold,
        "warning_threshold": warning_threshold,
        "burst_threshold": burst_threshold,
        "time_window": 30
    }
    port_scan_config = {
        "threshold": port_scan_threshold,
        "time_window": 30,
        "white_list": normal_ips
    }
    sql_config = {
        "keywords": {"SELECT", "FROM", "WHERE", "AND", "OR", "DROP", "INSERT", "DELETE", "/*", "*/", "--", ";"}
    }
    return MultiAttackDetector(ddos_config, port_scan_config, sql_config)

def parse_sql_input(sql_input):
    fsa = initialize_fsa()
    is_attack = fsa.detect_sql_injection(sql_input)
    print(f"[DETECT] SQL Injection detected: {is_attack}")
    return is_attack

def parse_ddos_requests(request_counts):
    fsa = initialize_fsa()
    for _ in range(request_counts):
        fsa.ddos_fsa.transition()
    print(f"[STATE] DDoS state: {fsa.ddos_fsa.state}")
    return fsa.ddos_fsa.is_attack_detected(), fsa.ddos_fsa.state

def parse_port_scan(scan_counts, ip):
    fsa = initialize_fsa()
    for _ in range(scan_counts):
        fsa.port_scan_fsa.transition(ip)
    print(f"[STATE] Port Scan state for {ip}: {fsa.port_scan_fsa.state}")
    return fsa.port_scan_fsa.is_attack_detected(ip)
