import json
import socket
import threading
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote_plus
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json

STORAGE_DIR = "storage"
STORAGE_FILE = os.path.join(STORAGE_DIR, "data.json")

# Створити каталог та файл, якщо не існує
os.makedirs(STORAGE_DIR, exist_ok=True)
if not os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "w") as f:
        json.dump({}, f, indent=2)


BASE_DIR = Path(__file__).parent
STORAGE_DIR = BASE_DIR / 'storage'
STATIC_DIR = BASE_DIR / 'static'
TEMPLATES_DIR = BASE_DIR / 'templates'

HOST = '127.0.0.1'
HTTP_PORT = 3000
SOCKET_PORT = 5000

STORAGE_DIR.mkdir(exist_ok=True)


def save_to_json(data):
    try:
        storage_file = STORAGE_DIR / 'data.json'
        if storage_file.exists():
            with open(storage_file, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        else:
            current_data = {}

        timestamp = str(datetime.now())
        current_data[timestamp] = data

        with open(storage_file, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save data: {e}")


def socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, SOCKET_PORT))
    print(f"Socket server running on {HOST}:{SOCKET_PORT}")

    while True:
        data, _ = sock.recvfrom(1024)
        decoded = unquote_plus(data.decode())
        print("Received socket data:", decoded)

        parts = decoded.split('&')
        payload = {}
        for part in parts:
            if '=' in part:
                key, value = part.split('=')
                payload[key] = value

        save_to_json(payload)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        route = self.path.split('?')[0]

        if route == '/':
            self.render_template('index.html')
        elif route == '/message':
            self.render_template('message.html')
        elif route.startswith('/static/'):
            self.serve_static_file(route)
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(content_length)

            # Send data to socket server
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data, (HOST, SOCKET_PORT))

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_error(404, "Page Not Found")

    def render_template(self, template_name):
        template_path = TEMPLATES_DIR / template_name
        if template_path.exists():
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(template_path.read_bytes())
        else:
            self.send_error(404, "Page Not Found")

    def serve_static_file(self, path):
        static_file_path = BASE_DIR / path.strip('/')
        if static_file_path.exists():
            self.send_response(200)
            if static_file_path.suffix == '.css':
                self.send_header('Content-type', 'text/css')
            elif static_file_path.suffix in ['.png', '.jpg', '.jpeg']:
                self.send_header('Content-type', f'image/{static_file_path.suffix[1:]}')
            else:
                self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(static_file_path.read_bytes())
        else:
            self.send_error(404, "Static file not found")


def run_http():
    server = HTTPServer((HOST, HTTP_PORT), SimpleHTTPRequestHandler)
    print(f"HTTP server running on http://{HOST}:{HTTP_PORT}")
    server.serve_forever()


def main():
    t1 = threading.Thread(target=run_http, daemon=True)
    t2 = threading.Thread(target=socket_server, daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
