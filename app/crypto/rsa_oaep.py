from hashlib import sha3_256
from random import randbytes
from typing import Tuple


def mgf1(seed: bytes, n_bytes: int, hash_func=sha3_256) -> bytes:
    """
    Mask Generation Function 1 (MGF1) using SHA-3.

    :param seed: Seed for the mask generation.
    :param length: Desired length of the mask.
    :param hash_func: Hash function to use (default: sha3_256).
    :return: Generated mask.
    """
    mask = b""
    counter = 0
    while len(mask) < n_bytes:
        c = counter.to_bytes(4, "big")
        mask += hash_func(seed + c).digest()
        counter += 1
    return mask[:n_bytes]


def oaep_pad(message_bytes: bytes, label: bytes = b"", n_bits: int = 1024) -> bytes:
    """
    Apply OAEP padding to a message.

    :param message: Message to pad.
    :param label: Optional label (default: empty).
    :param k: Length of the padded message.
    :return: Padded message.
    """
    n_bytes = n_bits // 8
    hash_len = sha3_256().digest_size
    m_len = len(message_bytes)

    if m_len > n_bytes - 2 * hash_len - 1:
        raise ValueError("Mensagem muito longa para o padding OAEP")

    l_hash = sha3_256(label).digest()
    ps = b"\x00" * (n_bytes - (m_len + 1) - 2 * hash_len - 1)
    db = l_hash + ps + b"\x01" + message_bytes
    seed = randbytes(hash_len)
    db_mask = mgf1(seed, n_bytes - hash_len - 1)
    masked_db = bytes(a ^ b for a, b in zip(db, db_mask))
    seed_mask = mgf1(masked_db, hash_len)
    masked_seed = bytes(a ^ b for a, b in zip(seed, seed_mask))
    return b"\x00" + masked_seed + masked_db


def oaep_unpad(
    padded_message_bytes: bytes, label: bytes = b"", n_bits: int = 1024
) -> bytes:
    """
    Remove OAEP padding from a message.

    :param padded_message: Padded message to unpad.
    :param label: Optional label (default: empty).
    :param k: Length of the padded message.
    :return: Unpadded message.
    """
    n_bytes = n_bits // 8
    hash_len = sha3_256().digest_size

    if len(padded_message_bytes) != n_bytes:
        raise ValueError("Tamanho inválido para OAEP unpadding")

    y, masked_seed, masked_db = (
        padded_message_bytes[0],
        padded_message_bytes[1 : 1 + hash_len],
        padded_message_bytes[1 + hash_len :],
    )
    if y != 0:
        raise ValueError("OAEP decoding falhou")

    seed_mask = mgf1(masked_db, hash_len)
    seed = bytes(a ^ b for a, b in zip(masked_seed, seed_mask))
    db_mask = mgf1(seed, n_bytes - hash_len - 1)
    db = bytes(a ^ b for a, b in zip(masked_db, db_mask))

    l_hash = sha3_256(label).digest()
    if db[:hash_len] != l_hash:
        raise ValueError("OAEP decoding falhou: label hash incorreto")

    index = db.find(b"\x01", hash_len)
    if index == -1:
        raise ValueError("OAEP decoding falhou: delimitador \x01 não encontrado")

    return db[index + 1 :]


def encrypt_rsa(message_bytes: bytes, key: Tuple[int, int], n_bits=1024) -> bytes:
    message_int = int.from_bytes(message_bytes, byteorder="big")
    dlog = pow(message_int, key[0], key[1])
    return dlog.to_bytes((n_bits * 2) // 8, byteorder="big")


def decrypt_rsa(message_bytes: bytes, key: Tuple[int, int], n_bits=1024) -> bytes:
    message_int = int.from_bytes(message_bytes, byteorder="big")
    dlog = pow(message_int, key[0], key[1])
    return dlog.to_bytes((n_bits) // 8, byteorder="big")
