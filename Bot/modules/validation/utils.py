import xxhash
import msgpack


class HashDict:
    """Hashing utilities"""

    @staticmethod
    async def get_dict_hash(data: dict) -> str:
        return xxhash.xxh64(msgpack.dumps(data, use_bin_type=True)).hexdigest()

    @staticmethod
    async def compare_hashes(hash1: str, hash2: str) -> bool:
        return hash1 == hash2
