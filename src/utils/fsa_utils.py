# src/fsa_utils.py

from src.fsa_detection import MultiAttackFSA

def initialize_fsa(normal_threshold=100, warning_threshold=200, port_scan_threshold=10, normal_ips=None, time_window=10):
    if normal_ips is None:
        normal_ips = []
    return MultiAttackFSA(normal_threshold, warning_threshold, port_scan_threshold, normal_ips, time_window)

def parse_sql_input(fsa, ip, sql_input):
    fsa.transition_sql(ip, sql_input)
    return fsa.is_sql_attack_detected(ip)

def parse_ddos_requests(fsa, ip, request_count):
    for _ in range(request_count):
        fsa.transition_ddos(ip)
    return fsa.is_ddos_attack_detected(ip)

def parse_port_scan(fsa, ip):
    fsa.transition_port_scan(ip)
    return fsa.is_port_scan_detected(ip)
