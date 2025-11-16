import http.server
import socketserver
import threading
import urllib.parse
import json
from datetime import datetime
import os
import mimetypes

# --- Конфігурація ---
HTTP_PORT = 3000
SOCKET_PORT = 5000
SOCKET_HOST = 'localhost'  # Або '127.0.0.1'
STORAGE_DIR = 'storage'
DATA_FILE = os.path.join(STORAGE_DIR, 'data.json')
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))  # Каталог для статичних файлів


# --- HTTP Server ---
class MyHandler(http.server.SimpleHTTPRequestHandler):
    # Карта шляхів до файлів
    ROUTES = {
        '/': 'index.html',
        '/message': 'message.html',
        '/error.html': 'error.html',  # Для 404 помилок
    }

    # Карта типів контенту для статичних файлів
    MIME_TYPES = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.png': 'image/png',
        '.ico': 'image/x-icon'
    }

    def do_GET(self):
        # Обробка статичних файлів
        if self.path.startswith('/style.css') or self.path.startswith('/logo.png'):
            self.send_static_file()
            return

        # Обробка маршрутів HTML-сторінок
        if self.path in self.ROUTES:
            self.send_html_file(self.ROUTES[self.path])
        else:
            self.send_html_file(self.ROUTES['/error.html'], 404)  # Помилка 404

    def send_html_file(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            with open(os.path.join(STATIC_DIR, filename), 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error_page()

    def send_static_file(self):
        file_path = os.path.join(STATIC_DIR, self.path[1:])  # Видаляємо початковий слэш

        # Визначаємо MIME-тип на основі розширення файлу
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'  # Тип за замовчуванням

        try:
            with open(file_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', mime_type)
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_html_file(self.ROUTES['/error.html'], 404)

    def send_error_page(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            with open(os.path.join(STATIC_DIR, 'error.html'), 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.wfile.write(b"<h1>404 Not Found - Error page missing!</h1>")

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Відправляємо дані на Socket сервер
            self.send_to_socket_server(post_data)

            # Перенаправлення на головну сторінку
            self.send_response(302)  # Found
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_html_file(self.ROUTES['/error.html'], 404)

    def send_to_socket_server(self, data):
        # Створення UDP сокету та відправка даних
        sock = socketserver.socket.socket(socketserver.socket.AF_INET, socketserver.socket.SOCK_DGRAM)
        try:
            sock.sendto(data, (SOCKET_HOST, SOCKET_PORT))
        finally:
            sock.close()


# --- Socket Server ---
class MyUDPHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        # Декодування та парсинг даних форми
        decoded_data = urllib.parse.unquote_plus(data.decode('utf-8'))
        form_data = {
            key: value for key, value in (item.split('=') for item in decoded_data.split('&'))
        }

        # Додавання часу отримання
        timestamp = datetime.now().isoformat()

        # Збереження у JSON файл
        self.save_to_json(timestamp, form_data)

        print(f"Received message from HTTP server: {form_data}")
        # Зазвичай UDP сервер не відправляє відповіді, але можна для підтвердження
        # socket.sendto(b"ACK", self.client_address)

    def save_to_json(self, timestamp, data):
        # Перевіряємо та створюємо директорію storage, якщо вона не існує
        if not os.path.exists(STORAGE_DIR):
            os.makedirs(STORAGE_DIR)

        # Завантажуємо існуючі дані або створюємо порожній словник
        existing_data = {}
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {}  # Якщо файл пошкоджений або порожній

        # Додаємо нові дані
        existing_data[timestamp] = data

        # Зберігаємо оновлені дані
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)


# --- Функції запуску серверів у потоках ---
def run_http_server():
    with http.server.HTTPServer(("", HTTP_PORT), MyHandler) as httpd:
        print(f"HTTP server started on port {HTTP_PORT}")
        httpd.serve_forever()


def run_socket_server():
    with socketserver.ThreadingUDPServer((SOCKET_HOST, SOCKET_PORT), MyUDPHandler) as server:
        print(f"Socket server started on {SOCKET_HOST}:{SOCKET_PORT}")
        server.serve_forever()


# --- Головна функція ---
def main():
    # Перевіряємо та створюємо директорію storage, якщо вона не існує
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
        print(f"Directory '{STORAGE_DIR}' created.")

    # Перевіряємо та створюємо порожній data.json, якщо він не існує
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        print(f"File '{DATA_FILE}' created.")

    http_thread = threading.Thread(target=run_http_server)
    socket_thread = threading.Thread(target=run_socket_server)

    http_thread.start()
    socket_thread.start()

    # Можна додати логіку для очікування завершення потоків,
    # або просто дозволити головному потоку завершитись,
    # а сервери будуть працювати у фоновому режимі до зупинки процесу.
    # Для простоти, залишимо їх працювати у фоні.
    # http_thread.join()
    # socket_thread.join()


if __name__ == "__main__":
    main()