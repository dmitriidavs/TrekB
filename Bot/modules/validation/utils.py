import os

import xxhash


async def gen_pointer(p_len: int = 8) -> str:
    """Generate a random hash pointer for message broker to use as part of a key"""

    rand_bytes = os.urandom(p_len)
    hash_val = xxhash.xxh32(rand_bytes).intdigest()

    return hex(hash_val)[2:p_len + 2]
