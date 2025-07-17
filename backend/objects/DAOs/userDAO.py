from db import get_db
from models.user import User


from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

import math, random




def get_all():
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("SELECT * FROM users")
            return [User(u) for u in db.fetchall()]
        

def get_user(id: int):
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("SELECT * FROM users WHERE user_id=%s", [id])
            return User(db.fetchall())
        

def signup(id, username, password):
    new_salt = get_random_bytes(64)
    salt_hex = new_salt.hex()

    computed_pass = PBKDF2(password, salt_hex, count=100000, hmac_hash_module=SHA512).hex()

    # generate a random avatar
    random_string = ''
    valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    n = math.floor( random.random() * 15 ) + 10
    while n > 0:
        randomString += valid_chars.charAt( math.floor( random.random() * len(valid_chars) ) )
        n=n-1
    avatar = 'https://robohash.org/${randomString}.png?size=64x64&set=set1&bgset=any'

    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("INSERT INTO users (user_id, user_name, user_pass, user_salt, user_avatar) VALUES (%s, %s, %s, %s, %s)", [id, username, computed_pass, salt_hex, avatar])
            conn.commit()
            db.execute("SELECT * FROM users WHERE user_id=%s", [id])
            return (['user added: '] + User(db.fetchall()).toString())
        

def login(username, password):
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("SELECT * FROM users WHERE user_name=%s", [username])
            user = User(db.fetchall())

            if (user and user.validate_pass(password)):
                return user
            
            raise Exception("invalid username/password combination")