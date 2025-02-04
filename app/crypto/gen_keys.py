import math
from random import getrandbits, randint
from typing import Tuple


def miller_rabin_test(n: int, k: int) -> bool:
    """
    Perform the Miller-Rabin primality test.

    :param n: The number to test for primality.
    :param k: The number of iterations to perform.
    :return: True if n is probably prime, False otherwise.
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        if x != n - 1:
            return False
    return True


def gen_large_prime(n_bits: int = 1024) -> int:
    """
    Generate a large prime number.

    :param n_bits: The number of bits for the prime number.
    :return: A large prime number.
    """
    while True:
        n = getrandbits(n_bits)
        if miller_rabin_test(n, 5):
            return n


def gen_coprime(n: int) -> int:
    """
    Generate a coprime integer.

    :param phi_n: The value of Euler's totient function.
    :return: A coprime integer.
    """
    while True:
        e = randint(2, n - 1)
        if math.gcd(e, n) == 1:
            return e


def gen_keys(n_bits: int = 1024) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Generate RSA public and private keys.

    :param n_bits: The number of bits for the keys.
    :return: A tuple containing the public key and private key.
    """
    p = gen_large_prime(n_bits)
    q = gen_large_prime(n_bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = gen_coprime(phi_n)
    d = pow(e, -1, phi_n)
    return (e, n), (d, n)  # Public Key, Private Key
