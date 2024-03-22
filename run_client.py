import sys
import time

from loguru import logger

from src.main.python.client import Client
from src.main.python.create_message import create_message

if __name__ == "__main__":
    # Verifica si se proporcionan los argumentos host y port
    if len(sys.argv) != 3:
        print("Uso: python run_client.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]  # Obtén el host del primer argumento
    logger.info(f"Host: {host}")
    logger.info(f"Port: {sys.argv[2]}")
    port = int(sys.argv[2])  # Obtén el puerto del segundo argumento (convertido a entero)

    # Crea una instancia del servidor con los valores proporcionados
    client = Client(host, port)
    client.connect()
    while True:
        time.sleep(0.001)
        client.send_message(create_message())
        print(client.receive_message())
        if input("Enviar otro mensaje? (s/n): ").lower() != "s":
            break
    client.close()
