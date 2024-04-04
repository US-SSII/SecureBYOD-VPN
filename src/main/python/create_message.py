# message_creator.py
import random
import string

from src.main.python.json_utils.json_message import JSONMessage

def create_message() -> str:
    """
    Creates a JSON message based on user input.

    Accepted actions are "register" and "message".

    Returns:
        str: A JSON message representing the action and the data provided by the user.
    """
    action = input("Accepted actions are:\n- register\n- message\nAction: ")
    if action == "register":
        message = JSONMessage(action, input("Username: "), input("Password: "), "Nothing")
    elif action == "message":
        message = JSONMessage(action, input("Username: "), input("Password: "), input("Message: "))
    else:
        raise ValueError("Invalid action")
    return message.to_json()


def random_message() -> JSONMessage:
    return JSONMessage(None, generate_random_string(50), generate_random_string(50), generate_random_string(50))


def generate_random_string(length: int) -> str:
    """
    Generates a random string of the specified length.

    Args:
        length (int): The length of the random string to be generated.

    Returns:
        str:The randomly generated string.
    """

    characters = string.ascii_letters + string.digits  # Puedes ajustar los caracteres permitidos según tus necesidades
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

if __name__ == "__main__":
    print(random_message())
