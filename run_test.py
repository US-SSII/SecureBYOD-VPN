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

# CONSTANTS
current_directory = os.path.dirname(os.path.abspath(__file__)) + "/src/main/resources"
configuration = ConfigParser()
configuration.read("configuration.ini")
keystores_path = os.path.join(current_directory, configuration.get("KEYSTORE", "path"))
port = int(configuration.get("SERVER", "port"))
host = configuration.get("SERVER", "host")
server_alias = configuration.get("SERVER", "alias")
common_name = configuration.get("SERVER", "common_name")
password_path = os.path.join(current_directory, "passwords.json")
message_path = os.path.join(current_directory, "messages.json")

if __name__ == "__main__":

    server = Server(host, port)
    thread_server = Thread(target=server.start)
    thread_server.start()
    time.sleep(1)
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

    password_manager = PasswordManager(password_path)
    logger.info(f"Number of users: {password_manager.get_num_passwords()}")

    message_manager = MessageManager(message_path)
    logger.info(f"Number of messages: {message_manager.get_num_messages()}")
