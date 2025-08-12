import json
import socket
import threading
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote_plus
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# Шляхи
BASE_DIR = Path(__file__).parent
STORAGE_DIR = BASE_DIR / 'storage'
STATIC_DIR = BASE_DIR / 'static'
TEMPLATES_DIR = BASE_DIR / 'templates'
STORAGE_FILE = STORAGE_DIR / 'data.json'

# Порти
HOST = '127.0.0.1'
HTTP_PORT = 3000
SOCKET_PORT = 5000

# Гарантуємо існування каталогу та JSON-файлу
STORAGE_DIR.mkdir(exist_ok=True)
if not STORAGE_FILE.exists():
    with open(STORAGE_FILE, 'w') as f:
        json.dump({}, f, indent=2, ensure_ascii=False)


def save_to_json(data: dict):
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
    except Exception:
        current_data = {}

    timestamp = str(datetime.now())
    current_data[timestamp] = data

    with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)


def socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, SOCKET_PORT))
    print(f"[SOCKET] Running on {HOST}:{SOCKET_PORT}")

    while True:
        data, _ = sock.recvfrom(4096)
        decoded = unquote_plus(data.decode())
        print("[SOCKET] Received:", decoded)

        parts = decoded.split('&')
        payload = {}
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
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
            self.render_template('error.html', status=404)

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(content_length)

            # Надсилаємо в socket-сервер
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data, (HOST, SOCKET_PORT))

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.render_template('error.html', status=404)

    def render_template(self, template_name, status=200):
        path = TEMPLATES_DIR / template_name
        if path.exists():
            self.send_response(status)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(path.read_bytes())
        else:
            self.send_error(404, "Template Not Found")

    def serve_static_file(self, route):
        path = BASE_DIR / route.lstrip('/')
        if path.exists():
            self.send_response(200)
            mime = self.guess_type(path.suffix)
            self.send_header('Content-Type', mime)
            self.end_headers()
            self.wfile.write(path.read_bytes())
        else:
            self.send_error(404, "Static file not found")

    def guess_type(self, ext):
        return {
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.svg': 'image/svg+xml'
        }.get(ext, 'application/octet-stream')


def run_http_server():
    server = HTTPServer((HOST, HTTP_PORT), SimpleHTTPRequestHandler)
    print(f"[HTTP] Running on http://{HOST}:{HTTP_PORT}")
    server.serve_forever()


def main():
    thread_http = threading.Thread(target=run_http_server, daemon=True)
    thread_socket = threading.Thread(target=socket_server, daemon=True)
    thread_http.start()
    thread_socket.start()
    thread_http.join()
    thread_socket.join()


if __name__ == '__main__':
    main()
