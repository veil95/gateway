import httpx
from errors import ChatServiceUnavailable, NotInChat, MessageNotFound, NotAuthor


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

    async def save_message(self, user_id: str, payload: dict):
        response = await self._make_request(
            method="POST",
            url="/api/messages/",
            json={
                "user_id": user_id,
                "chat_id": payload.get("chat_id"),
                "reply_to_message_id": payload.get("reply_to_message_id"),
                "data_type": "TextOrAttachments",
                "body": payload.get("body"),
            })

        if response.status_code == 403:
            raise NotInChat
        if response.is_success:
            return response.json()
        else:
            raise ChatServiceUnavailable

    async def delete_message(self, user_id: str, payload: dict):
        response = await self._make_request(
            method="DELETE",
            url=f"/api/messages/{payload.get("message_id")}",
            params={
                "user_id": user_id
            })
        if response.status_code == 404:
            raise MessageNotFound
        elif response.status_code == 403:
            raise NotAuthor
        elif response.is_success:
            return response.json()
        else:
            raise ChatServiceUnavailable

    async def edit_message(self, user_id: str, payload: dict):
        response = await self._make_request(
            method="PATCH",
            url=f"/api/messages/{payload.get("message_id")}",
            params={
                "user_id": user_id
            },
            json={
                "body": payload.get("body")
            }
        )
        if response.status_code == 404:
            raise MessageNotFound
        elif response.status_code == 403:
            raise NotAuthor
        elif response.is_success:
            return response.json()
        else:
            raise ChatServiceUnavailable

