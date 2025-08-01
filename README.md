**README.md**

````markdown
## Lightweight Python Port Scanner

A custom TCP port scanning tool built in Python, designed for fast, multithreaded reconnaissance. Features banner grabbing, HTTP header probing on common web ports, graceful interruption handling, and colored terminal output for better readability.

### Features

- **Multithreaded Scanning**: Uses `ThreadPoolExecutor` for concurrent TCP connect scans.
- **Banner Grabbing**: Retrieves service banners (SSH, FTP, SMTP, etc.) to help identify software versions.
- **HTTP Probing**: Sends `HEAD` requests on ports 80, 443, 8000, 8080, 8443 to capture HTTP status lines and server headers.
- **Graceful Shutdown**: Handles `KeyboardInterrupt` (Ctrl+C) to terminate scans cleanly.
- **Colored Output**: Employs Colorama to distinguish open ports, banners, and HTTP info in the console.
- **Flexible Configuration**: Customizable port ranges, timeout, thread count, and verbose logging.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GLPtrs/pyportscanner
   cd pyportscanner
````

2. **Create a virtual environment (optional but recommended)**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python3 port_scanner.py <target> [options]
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
  python3 port_scanner.py example.com
  ```

* **Scan ports 1–500 with banner grabbing**:

  ```bash
  python3 port_scanner.py example.com -p 1-500 -b
  ```

* **Full scan, HTTP probe, verbose output**:

  ```bash
  python3 port_scanner.py example.com -p 1-1024 -b -s -v
  ```
