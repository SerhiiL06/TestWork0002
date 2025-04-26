from dataclasses import dataclass


@dataclass
class RegisterUser:
    email: str
    password_1: str
    password_2: str
