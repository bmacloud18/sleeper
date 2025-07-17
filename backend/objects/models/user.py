from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

import math, random


class User:
    def __init__(self, user):
        self.id = user[0]
        self.username = user[1]
        self._passwordhash = user[2]
        self._salt = user[3]
        self.avatar = user[4]

    def __str__(self):
        return f"User: {self.id}, {self.username}, {self.avatar}"
    
    def validate_pass(self, password):
        digest = PBKDF2(password, self._salt, count=100000, hmac_hash_module=SHA512).hex()

        return self._passwordhash == digest