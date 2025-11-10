import hashlib
import struct
import time

def little_endian(hex_str):
    return bytes.fromhex(hex_str)[::-1]

def double_sha256(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()

def find_genesis(version, prev_block, merkle_root, timestamp, bits):
    target = (bits & 0xffffff) * (2 ** (8 * ((bits >> 24) - 3)))
    print(f"Target: {hex(target)}")

    for nonce in range(0, 0xffffffff):
        header = (
            struct.pack("<L", version) +
            little_endian(prev_block) +
            little_endian(merkle_root) +
            struct.pack("<LLL", timestamp, bits, nonce)
        )
        hash_ = double_sha256(header)[::-1]
        if int(hash_.hex(), 16) < target:
            print(f"✅ Found valid genesis block!")
            print(f"Nonce: {nonce}")
            print(f"Genesis Hash: {hash_.hex()}")
            print(f"Timestamp: {timestamp}")
            return nonce, hash_.hex()
        if nonce % 500000 == 0:
            print(f"Searching... nonce={nonce}")
    print("❌ No valid genesis found.")
    return None, None

if __name__ == "__main__":
    version = 1
    prev_block = "00" * 32
    merkle_root = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
    timestamp = int(time.time())  # waktu sekarang
    bits = 0x1e0ffff0             # difficulty ringan
    find_genesis(version, prev_block, merkle_root, timestamp, bits)
