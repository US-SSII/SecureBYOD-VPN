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
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TODO: Use SSL
        self.server_socket.bind((self.host, int(self.port)))
        self.server_socket.listen(5)
        load_logger(self.is_test)

        # threading.Thread(target=self.print_scheduler).start()
        # schedule.every(30).days.do(lambda: self.execute_non_blocking(create_report))
        logger.info("The server has started successfully.")

        self.running = True
        while self.running:
            logger.info("Waiting for incoming connections...")
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
                logger.info("Waiting for a message from the client...")
                active, _, _ = select.select([client_socket], [], [], 1)
                if not active:
                    continue

                data = client_socket.recv(1024)
                if not data:
                    break

                received_message = data.decode()
                message = self.actions(received_message)
                logger.info(f"Sending message: {message}")
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
        return received_message

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
            logger.info(f"Sending chunk: {chunk}")
            client_socket.sendall(chunk.encode("utf-8"))
        time.sleep(0.001)
        logger.info("Sending end of message")
        client_socket.sendall("END".encode("utf-8"))

    def stop(self) -> None:
        """
        Stop the server.
        """
        self.running = False
        self.server_socket.close()
        logger.info("The server has stopped successfully.")


