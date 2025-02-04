# Função para calcular o hash SHA-3
import base64
from hashlib import sha3_256
from typing import Tuple

from app.crypto import rsa_oaep


def calculate_hash(message: str) -> bytes:
    """
    Calculate the SHA-3 hash of a message.

    :param message: Message to hash
    :return: SHA-3 hash of the message
    """
    return sha3_256(message.encode()).digest()


def sign_message(message: str, private_key: Tuple[int, int]) -> str:
    message_hash = calculate_hash(message)
    padded_hash = rsa_oaep.oaep_pad(message_hash)
    signature_bytes = rsa_oaep.encrypt_rsa(padded_hash, private_key)
    return base64.b64encode(signature_bytes).decode()


def verify_message(message: str, signature: str, public_key: Tuple[int, int]) -> bool:
    signature_bytes = base64.b64decode(signature.encode())
    decrypted_hash = rsa_oaep.decrypt_rsa(signature_bytes, public_key)
    unpadded_hash = rsa_oaep.oaep_unpad(decrypted_hash)
    message_hash = calculate_hash(message)
    return unpadded_hash == message_hash
