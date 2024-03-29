# json_message.py
import json


class JSONMessage:
    def __init__(self, username: str, password: str, message: str) -> None:
        """
        Initializes a JSONMessage object.

        Args:
            username (str): The source account.
            password (str): The receiver account.
            message (str): The amount in the message.
        """
        self.username = username
        self.password = password
        self.message = message

    def to_dict(self) -> dict:
        """
        Converts the JSONMessage object to a dictionary.

        Returns:
            dict: The dictionary representation of the JSONMessage.
        """
        return {
            'username': self.username,
            'password': self.password,
            'message': self.message,
        }

    def to_json(self) -> str:
        """
        Converts the JSONMessage object to a JSON-formatted string.

        Returns:
            str: The JSON-formatted string.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

