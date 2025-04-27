import string
from random import randint

from passlib.context import CryptContext


class PasswordService:
    def __init__(self, bcrypt_context: CryptContext) -> None:
        self.bcrypt = bcrypt_context

    def validate_password(self, pw1: str, pw2: str) -> dict:
        password_errors = {}

        if not self.compare(pw1, pw2):
            password_errors["password"] = "Passwords do not match"
            return password_errors

        if len(pw1) < 8:
            password_errors["length"] = "Password must be at least 8 characters long"

        return password_errors

    @staticmethod
    def compare(first: str, second: str) -> bool:
        return first == second

    def hash_pw(self, pw: str) -> str:
        return self.bcrypt.hash(pw)

    def verify_pw(self, secret: str, hashed: str) -> bool:
        return self.bcrypt.verify(secret, hashed)
