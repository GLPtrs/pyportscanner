## ⚡ Lightweight Python Port Scanner

A fast and flexible TCP port scanner written in Python. Designed for quick reconnaissance, it supports multithreaded scanning, service banner detection, and lightweight HTTP probing. Ideal for security testing and network diagnostics.

### 🔍 Key Features

- **Concurrent Scanning**  
  Leverages Python's `ThreadPoolExecutor` to scan multiple ports in parallel for high performance.

- **Service Banner Grabbing**  
  Attempts to extract banners from open ports (e.g., SSH, FTP, SMTP) to help identify running services.

- **HTTP Header Analysis**  
  Automatically sends `HEAD` requests to common web ports (80, 443, 8000, 8080, 8443) to retrieve server info and status codes.

- **Interrupt Handling**  
  Gracefully stops on `Ctrl+C`, ensuring clean termination and user feedback.

- **Colorized Terminal Output**  
  Uses `Colorama` to highlight open ports, service banners, and HTTP headers for better readability.

- **Custom Configuration**  
  Easily adjust port ranges, timeouts, thread count, and verbosity through command-line arguments.

### ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GLPtrs/pyportscanner
   cd pyportscanner



2. **Create a virtual environment (optional but recommended)**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Make the script executable (or use /usr/bin/env python3 pyportscanner.py)**:
   ```bash
   chmod +x pyportscanner.py
   ```
**Usage**:
   ```bash
   ./pyportscanner.py <target> [options]
   ```

**Options:**

| Flag              | Description                                      |
| ----------------- | ------------------------------------------------ |
| `<target>`        | Hostname or IP address to scan                   |
| `-p`, `--ports`   | Ports/ranges to scan (e.g., `22,80` or `1-1024`) |
| `-t`, `--threads` | Maximum concurrent threads (default: 100)        |
| `--timeout`       | Connection timeout in seconds (default: 1.0)     |
| `-b`, `--banner`  | Enable banner grabbing                           |
| `-s`, `--service` | Enable HTTP HEAD probing on common web ports     |
| `-v`, `--verbose` | Enable verbose debug logging                     |

## Examples

* **Basic scan, default ports**:

  ```bash
  ./pyportscanner.py <IP>
  ```

* **Scan ports 1–500 with banner grabbing**:

  ```bash
  ./pyportscanner.py <IP> -p 1-500 -b
  ```

* **Full scan, HTTP probe, verbose output**:

  ```bash
  ./pyportscanner.py <IP> -p 1-1024 -b -s -v
  ```
