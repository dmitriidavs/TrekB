import xxhash
import msgpack


class HashDict:
    """Hashing utilities"""

    @staticmethod
    def get_dict_hash(data: dict) -> str:
        return xxhash.xxh64(msgpack.dumps(data, use_bin_type=True)).hexdigest()

    @staticmethod
    def compare_hashes(hash1: str, hash2: str) -> bool:
        return hash1 == hash2
