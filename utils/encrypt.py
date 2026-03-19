from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import base64, hashlib, os

# Derive a key from the password
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Encrypt the database file
def encrypt_file(file_name: str, password: str):
    salt = os.urandom(16)  # Generate a random salt
    key = derive_key(password, salt)
    cipher = Fernet(key)

    # Read and encrypt the file
    with open(file_name, 'rb') as file:
        original_data = file.read()
    encrypted_data = cipher.encrypt(original_data)

    # Write the salt and encrypted data to a new file
    with open(file_name, 'wb') as file:
        file.write(salt + encrypted_data)  # Store salt with encrypted data

# Decrypt the database file
def decrypt_file(file_name: str, password: str):
    with open(file_name, 'rb') as file:
        # Read the salt from the start
        salt = file.read(16)
        encrypted_data = file.read()
    
    key = derive_key(password, salt)
    cipher = Fernet(key)

    # Decrypt the file
    decrypted_data = cipher.decrypt(encrypted_data)

    # Write the decrypted data back to the file
    with open(file_name, 'wb') as file:
        file.write(decrypted_data)

