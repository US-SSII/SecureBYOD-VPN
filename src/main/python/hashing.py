import hashlib
import hmac
from configparser import ConfigParser
from datetime import datetime


def select_hash_algorithm(day: int) -> str:
    """
    Selects the hash algorithm based on the day of the month.

    Args:
        day (int): The day of the month.

    Returns:
        str: The selected hash algorithm ('sha512', 'sha3_384' or 'sha256').
    """
    if day % 3 == 0:
        return 'sha512'
    elif day % 3 == 1:
        return 'sha3_384'
    else:
        return 'sha256'

def calculate_mac(json_str: str, nonce: str, date_today: datetime) -> str:
    """
    Calculates the Message Authentication Code (MAC) for a JSON-formatted string using different algorithms.

    Args:
        json_str (str): The JSON-formatted string.
        nonce (str): The nonce value.
        date_today (datetime): The current date and time.

    Returns:
        str: The calculated MAC value.
    """
    day = int(date_today.strftime('%d'))

    # Read the token from the configuration file
    config = ConfigParser()
    config.read("config.ini")
    token = config.get("HASHING", "key")

    # Calculate the MAC using the hash and token
    selected_algorithms = select_hash_algorithm(day)

    order = [json_str, nonce] if day % 2 == 0 else [nonce, json_str]

    calculated_mac = hmac.new(token.encode(), ''.join(order).encode(), digestmod=selected_algorithms)

    return calculated_mac.hexdigest()

