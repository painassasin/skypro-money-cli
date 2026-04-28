import random
import string


def generate_random_hex(length: int) -> str:
    return ''.join(random.choice(string.hexdigits) for _ in range(length))
