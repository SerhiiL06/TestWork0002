import datetime as dt
from datetime import datetime, timedelta
from os import access

import jwt
from fastapi import HTTPException

from backend.infra.settings import env_config


class TokenService:
    def create_access_token(self, payload: dict) -> str:
        access_payload = payload.copy()
        access_payload["exp"] = datetime.now() + timedelta(minutes=5)
        token = jwt.encode(access_payload, env_config.SECRET_KEY, algorithm="HS256")
        return token

    def create_refresh_token(self, payload: dict) -> str:
        refresh_payload = payload.copy()
        refresh_payload["exp"] = datetime.now() + timedelta(days=10)
        token = jwt.encode(refresh_payload, env_config.SECRET_KEY, algorithm="HS256")
        return token

    def get_user_data(self, token: str, token_type: str = "access_token") -> dict:
        try:
            user_data = jwt.decode(
                token, env_config.SECRET_KEY, algorithms=["HS256"], leeway=3600
            )
        except jwt.exceptions.ExpiredSignatureError as _:
            raise HTTPException(401, f"{token_type} was expired")

        self._verify_token(user_data)

        return user_data

    def _verify_token(self, token_payload: dict) -> None:
        if datetime.fromtimestamp(token_payload.get("exp")) < datetime.now():
            raise jwt.exceptions.DecodeError("Token was expired")
