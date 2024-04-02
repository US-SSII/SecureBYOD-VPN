# message_creator.py
import random
import string

from src.main.python.json.json_message import JSONMessage

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


