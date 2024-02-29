import base64
import random
from string import ascii_letters


def random_file_prefix() -> str:
    return ''.join(
        random.choices(ascii_letters, k=random.randint(10, 20))
    )


def random_file_extension() -> str:
    return ''.join(
        random.choices(ascii_letters, k=random.randint(2, 5))
    )


def random_file_name() -> str:
    return f'{random_file_prefix()}.{random_file_extension()}'


def random_base64_data(size: int) -> str:
    print(f'Chunk len = {len(random.randbytes(size))}')
    return bytes.decode(base64.b64encode(random.randbytes(size)))
