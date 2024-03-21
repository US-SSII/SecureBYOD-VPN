import sys

from src.main.python.client import Client

if __name__ == "__main__":
    # Verifica si se proporcionan los argumentos host y port
    if len(sys.argv) != 3:
        print("Uso: python run_client.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]  # Obtén el host del primer argumento
    port = int(sys.argv[2])  # Obtén el puerto del segundo argumento (convertido a entero)

    # Crea una instancia del servidor con los valores proporcionados
    client = Client(host, port)
    client.connect()