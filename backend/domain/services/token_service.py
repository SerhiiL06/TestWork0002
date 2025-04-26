import datetime as dt
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from backend.infra.settings import env_config


class TokenService:
    def create_token(self, payload: dict) -> dict:
        payload["exp"] = datetime.now() + timedelta(minutes=30)
        token = jwt.encode(payload, env_config.SECRET_KEY, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}

    def get_token(self, token: str) -> dict:
        try:
            user_data = jwt.decode(
                token, env_config.SECRET_KEY, algorithms=["HS256"], leeway=3600
            )
        except jwt.exceptions.ExpiredSignatureError as e:
            raise HTTPException(401, "reload session")

        self._verify_token(user_data)

        return user_data

    def _verify_token(self, token_payload: dict) -> None:
        if datetime.fromtimestamp(token_payload.get("exp")) < datetime.now():
            raise jwt.exceptions.DecodeError("exp token")
