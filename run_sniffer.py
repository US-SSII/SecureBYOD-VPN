import time
from configparser import ConfigParser
from threading import Thread

from src.main.python.client import Client
from src.main.python.create_message import random_message, generate_random_string
from src.main.python.manager.message_manager import MessageManager
from src.main.python.manager.password_manager import PasswordManager
from src.main.python.server import Server
from loguru import logger
import os

from src.main.python.sniffer import TrafficCapture

# CONSTANTS
current_directory = os.path.dirname(os.path.abspath(__file__)) + "/src/main/resources"
configuration = ConfigParser()
configuration.read("configuration.ini")
keystores_path = os.path.join(current_directory, configuration.get("KEYSTORE", "path"))
port = int(configuration.get("SERVER", "port"))
host = configuration.get("SERVER", "host")
server_alias = configuration.get("SERVER", "alias")
common_name = configuration.get("SERVER", "common_name")
password_path = os.path.join(current_directory, "passwords.json_utils")
message_path = os.path.join(current_directory, "messages.json_utils")

if __name__ == "__main__":

    server = Server(host, port)
    thread_server = Thread(target=server.start)
    thread_server.start()
    time.sleep(1)
    sniffer = TrafficCapture(interface="lo")

    thread_sniffer = Thread(target=sniffer.start_capture, args=(host, port, host, port, "tls"))

    thread_sniffer.start()

    for _ in range(100):
        client = Client(host, port)
        client.connect()
        message = random_message()
        message.action = "register"
        client.send_message(message.to_json())
        logger.success(client.receive_message())
        message.action = "message"
        client.send_message(message.to_json())
        logger.success(client.receive_message())
        message.message = generate_random_string(50)
        client.send_message(message.to_json())
        logger.success(client.receive_message())
        client.close()

    sniffer.stop_capture()
    thread_sniffer.join()


