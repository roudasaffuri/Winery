from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve the encryption key
key = os.getenv("ENCRYPTION_KEY")


cipher_suite = Fernet(key.encode())  # Initialize Fernet with the key

def encode_string(input_string):
    """Encrypts the input string."""
    return cipher_suite.encrypt(input_string.encode())

def decode_string(encrypted_string):
    """Decrypts the input string."""
    return cipher_suite.decrypt(encrypted_string).decode()
