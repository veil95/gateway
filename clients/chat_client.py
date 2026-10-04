import httpx
from errors import ChatServiceUnavailable

class ChatClient:
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
            raise ChatServiceUnavailable("Chat service is unavailable")

    async def save_message(self):
        pass
