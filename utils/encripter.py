import jwt
from passlib.context import CryptContext

class Encripter:
    def __init__(self, key):
        self.key = key
        self.password_hasher = CryptContext(schemes=["bcrypt"])

    def encript(self, text):
        return text + self.key

    def decript(self, text):
        return text.replace(self.key, '')