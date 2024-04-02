import hmac
import json
from configparser import ConfigParser

config = ConfigParser()
config.read("configuration.ini")
token = config.get("HASHING", "key")


class PasswordManager:

    def __init__(self, path: str):
        self.path = path

    def check_password(self, username: str, password: str) -> bool:
        try:
            passwords = self._load_passwords()
        except FileNotFoundError:
            passwords = []
        encrypted = self.encrypt_password(password)
        dick = {"username": username, "password": encrypted}
        if str(dick) in passwords:
            return True
        else:
            return False

    def _load_passwords(self) -> list:
        """
        Load old nonces from the file.

        Returns:
            list: List of old nonces.
        """
        with open(self.path, "r") as file:
            return json.load(file)

    def save_pasword(self, username: str, password: str) -> None:
        passwords = self._load_passwords()
        encrypted = self.encrypt_password(password)
        dick = {"username": username, "password": encrypted}
        passwords.append(str(dick))
        with open(self.path, "w") as file:
            json.dump(passwords, file)

    def encrypt_password(self, password: str):
        ecrypted = hmac.new(token.encode(), password.encode(), digestmod='sha256')
        return ecrypted.hexdigest()
