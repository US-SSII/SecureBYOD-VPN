import json
import random

from src.main.python.client import Client


class MaliciousClient(Client):
    """
    The MaliciousClient class extends the Client class and overrides the send_message method to send a malicious message.
    """

    def send_message(self, message: str, keys: list=[]) -> None:
        """
        Sends a malicious message to the connected server.

        Args:
            message (str): The message to be sent.
            keys (list): The list of keys to alter in the message.
        """
        message = json.loads(message)
        for key in keys:
            value = message[key]
            if isinstance(value, str):
                message[key] = self.alter_string_message(value)
            elif isinstance(value, int):
                message[key] = self.alter_int_message(value)
            else:
                raise ValueError("Unsupported message type")

        message = json.dumps(message)
        super().send_message(message)

    def alter_string_message(self, message: str) -> str:
        """
        Alters the content of a string message before sending.

        Args:
            message (str): The original string message.

        Returns:
            str: The altered string message.
        """
        altered_message = self.invert_string(message)
        altered_message = self.replace_characters(altered_message, {'e': '3', 'o': '0', 's': '5'})
        altered_message = self.capitalize_words(altered_message)
        altered_message = self.toggle_case(altered_message)

        return altered_message

    def alter_int_message(self, number: int) -> int:
        """
        Alters the content of an integer message before sending.

        Args:
            number (int): The original integer message.

        Returns:
            int: The altered integer message.
        """
        altered_number = self.reverse_digits(number)
        altered_number = self.add_random_number(altered_number)
        altered_number = self.multiply_by_random(altered_number)

        return altered_number

    def invert_string(self, text: str) -> str:
        """
        Inverts the characters of a string.

        Args:
            text (str): The input string.

        Returns:
            str: The inverted string.
        """
        return text[::-1]

    def replace_characters(self, text: str, replacements: dict) -> str:
        """
        Replaces characters in a string based on the provided replacements.

        Args:
            text (str): The input string.
            replacements (dict): Dictionary of character replacements.

        Returns:
            str: The string with replaced characters.
        """
        for old_char, new_char in replacements.items():
            text = text.replace(old_char, new_char)
        return text

    def capitalize_words(self, text: str) -> str:
        """
        Capitalizes the first letter of each word in a string.

        Args:
            text (str): The input string.

        Returns:
            str: The string with capitalized words.
        """
        return ' '.join(word.capitalize() for word in text.split())

    def toggle_case(self, text: str) -> str:
        """
        Toggles the case of characters in a string.

        Args:
            text (str): The input string.

        Returns:
            str: The string with alternating uppercase and lowercase characters.
        """
        return ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))


    def reverse_digits(self, number: int) -> int:
        """
        Reverses the digits of an integer.

        Args:
            number (int): The input integer.

        Returns:
            int: The integer with reversed digits.
        """
        return int(str(number)[::-1])

    def add_random_number(self, number: int) -> int:
        """
        Adds a random number to the integer.

        Args:
            number (int): The input integer.

        Returns:
            int: The integer with an added random number.
        """
        random_addition = random.randint(1, 100)
        return number + random_addition

    def multiply_by_random(self, number: int) -> int:
        """
        Multiplies the integer by a random number.

        Args:
            number (int): The input integer.

        Returns:
            int: The integer multiplied by a random number.
        """
        random_multiplier = random.randint(2, 5)
        return number * random_multiplier


if __name__ == '__main__':
    client = MaliciousClient("asdasd", 12)

