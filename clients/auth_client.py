import httpx
from errors import AuthServiceUnavailable, UserNotFoundAuthService, InvalidToken, IncorrectCredential


class AuthClient:
    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url
        self.timeout = timeout

    async def _make_request(self,
                      method: str,
                      url: str,
                      *,
                      headers=None,
                      params=None,
                      json=None):
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json
                )

                return response
        except httpx.RequestError:
            raise AuthServiceUnavailable("Auth service is unavailable")

    async def get_current_user(self, token: str) -> dict | None:
        response = await self._make_request(method="GET", url="/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        if response.is_success:
            return response.json()
        if response.status_code == 404:
            raise UserNotFoundAuthService
        if response.status_code == 401:
            raise InvalidToken
        else:
            raise AuthServiceUnavailable

    async def user_login(self, username: str, password: str):
        response = await self._make_request(
            method="POST",
            url="/auth/login",
            json={
                "username": username,
                "password": password}
        )
        return response

    async def user_registration(self, username: str, password_plaintext: str, display_name: str):
        response = await self._make_request(
            method="POST",
            url="/auth/register",
            json={
                "username": username,
                "password_plaintext": password_plaintext,
                "display_name": display_name
            }
        )
        return response

    async def refresh_token(self, refresh_token: str):
        response = await self._make_request(
            method="POST",
            url="/auth/refresh",
            headers={
                "Cookie": f"refresh_token={refresh_token}"
            }
        )
        return response