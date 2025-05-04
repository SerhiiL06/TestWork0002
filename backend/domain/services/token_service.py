from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException


class TokenService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def create_access_token(self, payload: dict) -> str:
        access_payload = payload.copy()
        access_payload["exp"] = datetime.now() + timedelta(minutes=15)
        token = jwt.encode(access_payload, self.secret_key)
        return token

    def create_refresh_token(self, payload: dict) -> str:
        refresh_payload = payload.copy()
        refresh_payload["exp"] = datetime.now() + timedelta(days=10)
        token = jwt.encode(refresh_payload, self.secret_key)
        return token

    def get_data_from_token(self, token: str, token_type: str = "access_token") -> dict:
        try:
            user_data = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            raise HTTPException(401, "Invalid token")
        except jwt.exceptions.ExpiredSignatureError as _:
            raise HTTPException(401, f"{token_type} was expired")
        return user_data
