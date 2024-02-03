import socket
import concurrent.futures
import ipaddress

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
            print(f"Port {port} open on {ip}")
    except:
        pass

def scan_ip(ip):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # Replace 65535 with a smaller number if you want to scan fewer ports
        executor.map(lambda port: scan_port(ip, port), range(1, 65536))

def scan_network(network):
    for ip in ipaddress.IPv4Network(network, strict=False):
        scan_ip(str(ip))

if __name__ == "__main__":
    target_network = input("Enter IP address or network (e.g., 192.168.1.0/24): ")
    scan_network(target_network)
