import httpx
from errors import AuthServiceUnavailable, UserNotFoundAuthService, InvalidToken


class AuthClient:
    def __init__(self, http: httpx.AsyncClient):
        self._http = http

    async def _make_request(self,
                      method: str,
                      url: str,
                      *,
                      headers=None,
                      params=None,
                      json=None):
        try:
            response = await self._http.request(
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
