import json
import uuid

class NonceManager:
    """
    NonceManager: Manage nonces to prevent replay attacks.
    """

    def __init__(self, path_old_nonces: str):
        """
        Initialize NonceManager.

        Args:
            path_old_nonces (str): Path to the file storing old nonces.
        """
        self.path_old_nonces = path_old_nonces

    def generate(self) -> str:
        """
        Generate a new nonce.

        Returns:
            str: Newly generated nonce.
        """
        return str(uuid.uuid4())

    def not_repeated(self, nonce: str) -> bool:
        """
        Check if the nonce is not repeated and update the file accordingly.

        Args:
            nonce (str): Nonce to check.

        Returns:
            bool: True if the nonce is not repeated, False otherwise.
        """
        try:
            old_nonces = self._load_old_nonces()
        except FileNotFoundError:
            old_nonces = []

        if nonce in old_nonces:
            return False
        else:
            old_nonces.append(nonce)
            self._save_old_nonces(old_nonces)
            return True

    def _load_old_nonces(self) -> list:
        """
        Load old nonces from the file.

        Returns:
            list: List of old nonces.
        """
        with open(self.path_old_nonces, "r") as file:
            return json.load(file)

    def _save_old_nonces(self, old_nonces: list) -> None:
        """
        Save old nonces to the file.

        Args:
            old_nonces (list): List of old nonces.
        """
        with open(self.path_old_nonces, "w") as file:
            json.dump(old_nonces, file)


