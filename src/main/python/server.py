import concurrent.futures
import json
import os
import socket
import threading
import time
from datetime import datetime

import schedule
import select
from loguru import logger

from src.main.python.integrity_verifier import validate_message
from src.main.python.logger import load_logger
from src.main.python.nonce import NonceManager
from src.main.python.statistics import create_report

current_directory = os.path.dirname(os.path.abspath(__file__))

class Server:
    def __init__(self, host: str, port: int, is_test: bool = False) -> None:
        """
        Initialize the server with the specified host and port.

        Args:
            host (str): The hostname or IP address to bind to.
            port (int): The port number to listen on.
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_test = is_test
        self.running = False

    def start(self) -> None:
        """
        Start the server listening for incoming connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, int(self.port)))
        self.server_socket.listen(5)
        load_logger(self.is_test)

        threading.Thread(target=self.print_scheduler).start()
        schedule.every(30).days.do(lambda: self.execute_non_blocking(create_report))
        logger.info("The server has started successfully.")

        self.running = True
        while self.running:
            try:
                client_socket, _ = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except Exception:
                break

        logger.info("The server has been shut down successfully.")

    def handle_client(self, client_socket: socket) -> None:
        """
        Handle an incoming client connection by sending a response to any messages it sends.

        Args:
            client_socket (socket): The socket for the incoming connection.
        """
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
            print(e.with_traceback())
            logger.error(f"Error: {e}")
        finally:
            client_socket.close()
            logger.info("Client connection closed.")

    def actions(self, received_message: str) -> str:
        """
        Orchestrates a series of actions based on the received message.

        Returns:
            str: Server response to the client.
        """

        nonce_manager = NonceManager(os.path.join(current_directory, "../resources/nonces.json"))
        message_dict = json.loads(received_message)
        mac = message_dict.pop("mac")
        nonce = message_dict.pop("nonce")
        date = datetime.strptime(message_dict.pop("date"), "%Y-%m-%d %H:%M:%S.%f")
        json_str = json.dumps(message_dict, ensure_ascii=False)
        message = f"{message_dict['origin_account']} - {message_dict['receiver_account']} - {message_dict['amount']}"

        modification_attack = not validate_message(json_str, nonce, date, mac)
        replay_attack = not nonce_manager.not_repeated(nonce)

        if not modification_attack and not replay_attack:
            logger.success(f"Message received successfully: {message}")
            message = f"Received message: {message}"
        elif modification_attack and replay_attack:
            logger.error(f"Message has been modified and is a replay: {message}")
            message = "Message has been modified and is a replay."
        elif modification_attack:
            logger.error(f"Message has been modified: {message}")
            message = "Message has been modified."
        elif replay_attack:
            logger.error(f"Message is a replay: {message}")
            message = "Message is a replay."
        return message

    def execute_non_blocking(self, func: callable) -> None:
        """
        Execute a function in a separate thread.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(func)

    def print_scheduler(self) -> None:
        """
        Print "hello" every second.
        """
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def send_message_in_chunks(self, client_socket: socket, message: str) -> None:
        """
        Send a message to the client in chunks.

        Args:
            client_socket (socket): The socket for the connection.
            message (str): The message to send.
        """
        chunk_size = 512
        for i in range(0, len(message), chunk_size):
            chunk = message[i:i + chunk_size]
            client_socket.sendall(chunk.encode("utf-8"))

        client_socket.sendall("END".encode("utf-8"))

    def stop(self) -> None:
        """
        Stop the server.
        """
        self.running = False
        self.server_socket.close()
        logger.info("The server has stopped successfully.")


