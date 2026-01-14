from typing import List
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def decrypt_data(cyphertext: bytes, key: bytes) -> List[str]:
    iv = cyphertext[:AES.block_size]
    cyphertext = cyphertext[AES.block_size:]

    cypher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cypher.decrypt(cyphertext), AES.block_size)

    return plaintext.decode('utf-8').split('\n')


def encrypt_data(lines: List[str], key: bytes) -> bytes:
    plaintext = '\n'.join(lines).encode('utf-8')
    iv = get_random_bytes(AES.block_size)
    cypher = AES.new(key, AES.MODE_CBC, iv)
    cyphertext = cypher.encrypt(pad(plaintext, AES.block_size))
    return iv + cyphertext


def compute_sha256(s: str) -> bytes:
    return hashlib.sha256(s.encode('utf-8')).digest()
