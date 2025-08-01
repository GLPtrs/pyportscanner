#!/usr/bin/env python3

import argparse
import socket
import sys
import logging

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from colorama import init, Fore, Style

init(autoreset=True)

HTTP_PORTS = {80, 443, 8080, 8000, 8443}

class PortScanner:
    def __init__(self, target, ports, timeout, max_workers, enable_banner,
                verbose, http_probe):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.max_workers = max_workers
        self.enable_banner = enable_banner
        self.verbose = verbose
        self.http_probe = http_probe    
        self.ip = self.resolve_target()
        self.results = []
        self.configure_logging(verbose)

    def resolve_target(self):
        try:
            return socket.gethostbyname(self.target)
        except socket.gaierror:
            logging.error(f"Unable to resolve host: {self.target}")
            raise SystemExit
        
    def configure_logging(self, verbose):
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H%M%S",
            level=level
        )

    @staticmethod
    def parse_ports(port_str):
        ports = set()
        for part in port_str.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end+1))
            else:
                ports.add(int(part))
        return sorted(p for p in ports if 1 <= p <= 65535)

    def scan_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((self.ip, port))
                return port, True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return port, False
        
    def grab_banner(self, port):
        try: 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((self.ip, port))
                data = sock.recv(2048)
                return data.strip().decode(errors="ignore") if data else None
        except Exception:
            return None
        
    def probe_http(self, port):
        if port not in HTTP_PORTS:
            return None
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((self.ip, port))
                sock.sendall(b"HEAD / HTTP/1.0\r\nHost: %b\r\n\r\n" % self.target.encode())
                resp = sock.recv(2048)
                return resp.decode(errors="ignore").split("\r\n")[0]
        except Exception:
            return None
        
    def run(self):
        logging.info(
            f"Starting scan on {self.target} ({self.ip}, ports: {self.ip})"
        )
        start = datetime.now()
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(self.scan_port, port): port for port in self.ports}
                for future in as_completed(futures):
                    port = futures[future]
                    try:
                        _, open_ = future.result()
                    except Exception as e:
                        logging.debug(f"Port scan error - {port} : {e}")
                        continue

                    banner = None
                    http_info = None
                    if open_:
                        if self.enable_banner:
                            banner = self.grab_banner(port)
                        if self.http_probe:
                            http_info = self.probe_http(port)
                        logging.info(f"Port {port} is OPEN")
                    else:
                        logging.debug(f"Port {port} is CLOSED")

                    self.results.append({
                        'port': port,
                        'open': open_,
                        'banner': banner,
                        'http': http_info
                    })
        except KeyboardInterrupt:
            logging.info("Scan interrupted by user (Ctrl+C). Shutting down...")
            executor.shutdown(wait=False, cancel_futures=True)
            return
        duration = (datetime.now() - start).total_seconds()
        logging.info(f"Scan lasts {duration:.2f} seconds")
        self.print_results()

    def print_results(self):
        print(Style.BRIGHT + '\n === Scan Results ===')
        for r in sorted(self.results, key=lambda x: x['port']):
            if r["open"]:
                line = Fore.GREEN + f"-> {r['port']} OPEN" + Style.RESET_ALL
                if self.enable_banner and r['banner']:
                    line += Fore.CYAN + f" | Banner: {r['banner']}" + Style.RESET_ALL
                if self.http_probe and r['http']:
                    line += Fore.MAGENTA + f" | HTTP: {r['http']}" + Style.RESET_ALL
                print(line)
        if not any(r['open'] for r in self.results):
            print(Fore.RED + 'No open ports detected.' + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(description="Lightweight Python Port Scanner with Banner Grabbing & HTTP Probing")
    parser.add_argument("target", help="IP or domain for scanning")
    parser.add_argument("-p", "--ports", default="1-1024", help="Ports to scan, e.g., 22,80 or range 1-1024")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Max concurrent threads")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds")
    parser.add_argument("-b", "--banner", action="store_true", help="Grab service banners")
    parser.add_argument("-s", "--service", action="store_true", help="HTTP HEAD probing on standard web ports")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug logging")
    args = parser.parse_args()

    ports = PortScanner.parse_ports(args.ports)
    scanner = PortScanner(
        target=args.target,
        ports=ports,
        timeout=args.timeout,
        max_workers=args.threads,
        enable_banner=args.banner,
        verbose=args.verbose,
        http_probe=args.service
    )
    try:
        scanner.run()
    except KeyboardInterrupt:
        print("\nScan cancelled by user.")
        sys.exit()

if __name__ == "__main__":
    main()