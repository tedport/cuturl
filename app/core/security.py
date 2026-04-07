from pwdlib import PasswordHash
from pwdlib.hashers import bcrypt

_pw_hash = PasswordHash(hashers=[bcrypt.BcryptHasher()])

def verify_password(plain_password, hashed_password):
    return _pw_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return _pw_hash.hash(password)