from dataclasses import dataclass


@dataclass
class RegisterUser:
    name: str
    email: str
    password_1: str
    password_2: str
