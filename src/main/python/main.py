from threading import Thread

from src.main.python.client import Client
from src.main.python.keystore import create_keystore
from src.main.python.server import Server

if __name__ == "__main__":
    port = 12345
    host = "127.0.0.1"

    create_keystore()

    server = Server(host, port)
    thread_server = Thread(target=server.start)
    thread_server.start()

    client = Client(host, port)
    client.connect()
    client.send_message("Hello, server!")
    print(client.receive_message())
    client.close()
    thread_server.join()