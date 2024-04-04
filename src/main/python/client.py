import socket

import OpenSSL
from OpenSSL import SSL
from loguru import logger


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
        ctx = SSL.Context(SSL.TLS_METHOD)
        ctx.set_options(SSL.OP_NO_SSLv2 | SSL.OP_NO_SSLv3 | SSL.OP_NO_TLSv1 | SSL.OP_NO_TLSv1_1)
        ctx.set_min_proto_version(SSL.TLS1_3_VERSION)
        #cipher_suite = "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384"
        #context.set_cipher_list(cipher_suite)
        self.client_socket = OpenSSL.SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
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
