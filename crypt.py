import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


class FernetCrypt:
    """
    A utility class for handling Fernet encryption and decryption.
    """

    def __init__(self):
        self.__salt_bytes = None
        self.__set_salt()

    def __set_salt(self):
        salt = os.environ.get("DATABASE_PASSWORD")
        if salt is None:
            raise ValueError("DATABASE_PASSWORD environment variable not set")
        self.__salt_bytes = salt.encode("utf-8")

    def get_fernet(self) -> Fernet:
        """
        Get a Fernet object for encryption and decryption.
        """

        # Get user password
        input_string = input("Enter your master password: ")
        input_bytes = input_string.encode("utf-8")

        # Create a key derivation function
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            iterations=100000,
            salt=self.__salt_bytes,
            backend=default_backend()
        )

        # Derive the user key and encode it in URL-safe base64 for use with Fernet
        key = kdf.derive(input_bytes)
        fernet_key = base64.urlsafe_b64encode(key)
        return Fernet(fernet_key)
