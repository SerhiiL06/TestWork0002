import string
from random import randint

from passlib.context import CryptContext


class PasswordService:
    def __init__(self, bcrypt_context: CryptContext) -> None:
        self.bcrypt = bcrypt_context

    def validate_password(self, pw1: str, pw2: str) -> dict:
        password_errors = {}

        if not self.compare(pw1, pw2):
            password_errors["password"] = "compare password error"
            return password_errors

        if len(pw1) < 8:
            password_errors["length"] = "password mush have min 8 length"

        return password_errors

    @staticmethod
    def compare(first: str, second: str) -> bool:
        return first == second

    def hashing(self, pw: str) -> str:
        return self.bcrypt.hash(pw)

    def verify(self, secret: str, hashed: str) -> bool:
        return self.bcrypt.verify(secret, hashed)
