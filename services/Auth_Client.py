from typing import Dict
from fastapi import Cookie
from httpx import AsyncClient
from model.Exceptions import AuthError


base_url = "http://127.0.0.1:8001"


async def get_current_user(token: str) -> Dict:
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.status_code < 400:
            return response.json()
        raise AuthError()
