"""This module encrypts passwords."""
import hashlib


def encode_password(password):
    """This class encrypts passwords."""
    password = password.encode()
    password_encode = hashlib.sha256(password).hexdigest()
    return password_encode
