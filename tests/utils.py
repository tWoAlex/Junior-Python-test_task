import base64
import random
from string import ascii_letters


def random_file_name() -> str:
    prefix = ''.join(
        random.choices(ascii_letters, k=random.randint(10, 20))
    )
    suffix = ''.join(
        random.choices(ascii_letters, k=random.randint(2, 5))
    )
    return '.'.join((prefix, suffix))


def random_base64_data(size: int) -> str:
    print(f'Chunk len = {len(random.randbytes(size))}')
    return bytes.decode(base64.b64encode(random.randbytes(size)))
