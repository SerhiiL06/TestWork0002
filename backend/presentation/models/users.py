from dataclasses import dataclass


@dataclass
class RegisterUser:
    email: str
    hashed_password: str
