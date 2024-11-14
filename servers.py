from handler import HTTPHandler
from http.server import HTTPServer
from pathlib import Path
import json
import socket

class DataStorage():
    BASE_STORAGE_PATH = Path(__file__).parent / 'storage/'
    DATA_FILE = "data.json"

    def init_data_file(self):
        if not self.BASE_STORAGE_PATH.is_file():
            self.BASE_STORAGE_PATH.mkdir(parents=True, exist_ok=True)

        file_path = self.BASE_STORAGE_PATH / self.DATA_FILE
        
        if not file_path.is_file():
            with open(file_path, "w", encoding="utf-8") as fp:
                json.dump({}, fp)

    def save_data(self, data: dict) -> bool:
        filename = self.BASE_STORAGE_PATH / self.DATA_FILE

        with open(filename, "r", encoding="utf=8") as file:
            loaded_data = json.load(file)
        
        data = json.loads(data)
        loaded_data.update(data)

        with open(filename, "w", encoding="utf-8") as file:
            data = json.dump(loaded_data, file, ensure_ascii=False, indent=2)      

def socket_server(ip, port, data_storage: DataStorage):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        server = (ip, port)
        sock.bind(server)

        print(f"Socket UDP server runs on port {port}")

        try:
            while True:
                data, address = sock.recvfrom(1024)
                print(f"Received data from address {address}")
                data_storage.save_data(data.decode())
        except KeyboardInterrupt:
            print("Server is shutting down ...")
            
def run_socket_server():
    data_storage = DataStorage()
    data_storage.init_data_file()
    socket_server('127.0.0.1', 5000, data_storage)

def run_http_server(server=HTTPServer, handler=HTTPHandler):
    address = ("", 3000)

    http_server = server(address, handler)
    try:
        while True:
            http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
