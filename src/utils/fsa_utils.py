

def initialize_fsa(normal_threshold, warning_threshold, port_scan_threshold, normal_ips):
    from fsa_detection import MultiAttackFSA
    return MultiAttackFSA(normal_threshold, warning_threshold, port_scan_threshold, normal_ips)

def parse_sql_input(sql_input):
    fsa = initialize_fsa(normal_threshold=100, warning_threshold=200, port_scan_threshold=10, normal_ips=[])
    for char in sql_input:
        fsa.transition_sql(char)
    return fsa.is_sql_attack_detected()

def parse_ddos_requests(request_counts):
    fsa = initialize_fsa(normal_threshold=100, warning_threshold=200, port_scan_threshold=10, normal_ips=[])
    for count in request_counts:
        fsa.transition_ddos(count)
    return fsa.is_ddos_attack_detected()

def parse_port_scan(scan_counts, ip):
    
    normal_ips = []  
    fsa = initialize_fsa(normal_threshold=100, warning_threshold=200, port_scan_threshold=10, normal_ips=normal_ips)
    for count in scan_counts:
        fsa.transition_port_scan(ip, count) 
    return fsa.is_port_scan_detected()