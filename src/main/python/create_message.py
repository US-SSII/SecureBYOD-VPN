# message_creator.py
import random
import string

from src.main.python.json_message import JSONMessage

def create_message() -> str:
    """
    Creates a JSON message with a MAC summary.

    Returns:
        str: JSON message with MAC summary.
    """
    message = JSONMessage(input("Source account: "), input("Receiver account: "), input("Amount: "))
    return message.to_json()

def random_message() -> str:
    """
    Creates a random JSON message with a MAC summary.

    Returns:
        str: Random JSON message with MAC summary.
    """
    message = JSONMessage(generate_random_string(50), generate_random_string(50), random.randint(0, 1000))
    return message.to_json()

def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # Puedes ajustar los caracteres permitidos según tus necesidades
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

if __name__ == "__main__":
    print(random_message())