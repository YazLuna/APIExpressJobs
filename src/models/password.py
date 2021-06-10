import hashlib


def encode_password(password):
    password = password.encode()
    password_encode = hashlib.sha256(password).hexdigest()
    return password_encode


