import socket
import json
import os
from datetime import datetime
from flask import Flask, request, redirect, render_template, send_from_directory
from threading import Thread

app = Flask(__name__, static_folder='static', template_folder='templates')
UDP_IP = "127.0.0.1"
UDP_PORT = 5000
STORAGE_DIR = "storage"
DATA_FILE = os.path.join(STORAGE_DIR, "data.json")

# Ensure storage directory and data file exist
os.makedirs(STORAGE_DIR, exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        username = request.form.get("username")
        message = request.form.get("message")
        if not username or not message:
            return render_template("message.html", error="Please fill all fields")

        data = json.dumps({"username": username, "message": message})
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data.encode("utf-8"), (UDP_IP, UDP_PORT))
        return redirect("/")
    return render_template("message.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html"), 404

def socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"[Socket] Listening on {UDP_IP}:{UDP_PORT}")

    while True:
        data, _ = sock.recvfrom(1024)
        try:
            msg = json.loads(data.decode("utf-8"))
            timestamp = str(datetime.now())

            with open(DATA_FILE, "r", encoding="utf-8") as f:
                current_data = json.load(f)

            current_data[timestamp] = msg

            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(current_data, f, indent=2)

        except Exception as ex:
            print(f"[Socket Error] {ex}")

if __name__ == "__main__":
    Thread(target=socket_server, daemon=True).start()
    app.run(port=3000)
