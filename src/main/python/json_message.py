# json_message.py
import json
from datetime import datetime
from src.main.python.hashing import calculate_mac
from src.main.python.nonce import NonceManager

class JSONMessage:
    def __init__(self, origin_account: str, receiver_account: str, amount: str) -> None:
        """
        Initializes a JSONMessage object.

        Args:
            origin_account (str): The source account.
            receiver_account (str): The receiver account.
            amount (str): The amount in the message.
        """
        self.origin_account = origin_account
        self.receiver_account = receiver_account
        self.amount = amount
        self.nonce_manager = NonceManager("../resources/nonces.json")
        self.date: datetime = None
        self.date: datetime = self.get_current_date()
        self.mac: str = None

    def to_dict(self) -> dict:
        """
        Converts the JSONMessage object to a dictionary.

        Returns:
            dict: The dictionary representation of the JSONMessage.
        """
        nonce = self.nonce_manager.generate()
        return {
            'origin_account': self.origin_account,
            'receiver_account': self.receiver_account,
            'amount': self.amount,
            'nonce': nonce,
            'date': str(self.date),
            'mac': self.calculate_mac(nonce)
        }

    def to_micro_dict(self) -> dict:
        """
        Converts the JSONMessage object to a simplified dictionary.

        Returns:
            dict: The dictionary representation of the JSONMessage.
        """
        return {
            'origin_account': self.origin_account,
            'receiver_account': self.receiver_account,
            'amount': self.amount,
        }

    def to_json(self) -> str:
        """
        Converts the JSONMessage object to a JSON-formatted string.

        Returns:
            str: The JSON-formatted string.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def get_current_date(self) -> datetime:
        """
        Gets the current date and time.

        Returns:
            datetime: The current date and time.
        """
        if not self.date:
            self.date = datetime.now()
        return self.date

    def calculate_mac(self, nonce: str) -> str:
        """
        Calculates the Message Authentication Code (MAC) for the JSONMessage.

        Args:
            nonce (str): The nonce value for the calculation.

        Returns:
            str: The MAC value.
        """
        if not self.mac:
            json_str = json.dumps(self.to_micro_dict(), ensure_ascii=False)
            self.mac = calculate_mac(json_str, nonce, self.date)
        return self.mac

