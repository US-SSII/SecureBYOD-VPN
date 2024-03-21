import socket

import OpenSSL
from loguru import logger
from OpenSSL import SSL
from OpenSSL.SSL import ZeroReturnError


class Client:
    """
    The Client class facilitates communication with a server using a socket connection.
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Initializes a Client instance with the specified host and port.

        Args:
            host (str): Hostname or IP address of the server.
            port (int): Port number for the connection.
        """
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self) -> None:
        """
        Establishes a secure connection to the server using SSL/TLS.
        """
        context= OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
        self.client_socket = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.client_socket.connect((self.host, self.port))
        logger.info(f"Connected to {self.host}:{self.port} securely")

    def send_message(self, message: str) -> None:
        """
        Sends a message to the connected server.

        Args:
            message (str): The message to be sent.

        Raises:
            ConnectionError: If the connection is not established.
        """
        if not self.client_socket:
            raise ConnectionError("Connection not established. Call connect() first.")

        try:
            self.client_socket.sendall(message.encode())
            # Add any additional logic here, such as waiting for a response from the server
        except Exception as e:
            logger.error(f"Error sending message: {e}")

    def receive_message(self) -> str:
        """
        Receives a message from the connected server.

        Returns:
            str: The message received.

        Raises:
            ConnectionError: If the connection is not established.
        """
        if not self.client_socket:
            raise ConnectionError("Connection not established. Call connect() first.")

        try:
            message = ""
            while True:
                data = self.client_socket.recv(1024).decode()  # Receive data from the client
                logger.info(f"Received data: {data}")
                if not data:
                    logger.info("Connection closed by the server")
                    break
                if "END" in data:
                    logger.info("End of message")
                    break
                message += data
            return message
        except Exception as e:
            logger.error(f"Error receiving message: {e}")

    def close(self) -> None:
        """
        Closes the connection with the server.
        """
        if self.client_socket:
            self.client_socket.shutdown()
            self.client_socket.close()
            logger.info("Connection closed")

