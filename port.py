import socket
import concurrent.futures
import ipaddress
import argparse

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                print(f"Port {port} open on {ip}")
    except Exception as e:
        pass

def scan_ip(ip):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # Replace 65535 with a smaller number if you want to scan fewer ports
        executor.map(lambda port: scan_port(ip, port), range(1, 65536))

def scan_network(network):
    for ip in ipaddress.IPv4Network(network, strict=False):
        print(f"Scanning IP: {ip}")
        scan_ip(str(ip))

def main():
    parser = argparse.ArgumentParser(description='Simple Port Scanner')
    parser.add_argument('network', type=str, help='IP address or network (e.g., 192.168.1.0/24)')
    args = parser.parse_args()

    scan_network(args.network)

if __name__ == "__main__":
    main()
