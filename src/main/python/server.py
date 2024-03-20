import os
import socket
import threading
import time

import select
from OpenSSL import SSL
from loguru import logger

from src.main.python.generate_creatificates_and_keys import generate_key_pair, generate_certificate, \
    save_key_and_certificate

current_directory = os.path.dirname(os.path.abspath(__file__))


class Server:
    def __init__(self, host: str, port: int, is_test: bool = False) -> None:
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_test = is_test
        self.running = False

    def load_certificate(self) -> SSL.Context:
        """
        Load SSL certificate and private key for the server.
        """
        context = SSL.Context(SSL.SSLv23_METHOD)
        context.set_options(SSL.OP_NO_SSLv2 | SSL.OP_NO_SSLv3)

        cert_file = os.path.join(current_directory, "../resources/server.crt")
        key_file = os.path.join(current_directory, "../resources/server.key")

        # Comprueba si existen esos archivos
        if not os.path.exists(cert_file) or not os.path.exists(key_file):
            logger.error(f"Certificate or key files not found: {cert_file} and {key_file}")
            server_key = generate_key_pair()
            server_cert = generate_certificate(server_key, "server.example.com")
            save_key_and_certificate(server_key, server_cert, cert_file, key_file)

        context.use_privatekey_file(key_file, SSL.FILETYPE_PEM)
        context.use_certificate_file(cert_file)

        return context

    def start(self) -> None:
        context = self.load_certificate()

        self.server_socket = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.server_socket.bind((self.host, int(self.port)))

        self.server_socket.listen(5)

        self.running = True
        while self.running:
            try:
                client_socket, _ = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except Exception as e:
                logger.error(f"Error accepting connection: {e}")
                break

    def handle_client(self, client_socket: socket) -> None:
        try:
            while True:
                active, _, _ = select.select([client_socket], [], [], 1)
                if not active:
                    continue

                data = client_socket.recv(1024)
                if not data:
                    break

                received_message = data.decode()
                message = self.actions(received_message)
                self.send_message_in_chunks(client_socket, message)

        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            client_socket.close()

    def actions(self, received_message: str) -> str:
        return received_message

    def send_message_in_chunks(self, client_socket: socket, message: str) -> None:
        chunk_size = 512
        for i in range(0, len(message), chunk_size):
            chunk = message[i:i + chunk_size]
            client_socket.sendall(chunk.encode("utf-8"))
        time.sleep(0.001)
        client_socket.sendall("END".encode("utf-8"))

    def stop(self) -> None:
        self.running = False
        self.server_socket.close()