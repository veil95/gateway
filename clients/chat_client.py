import httpx
from errors import ChatServiceUnavailable, NotInChat, MessageNotFound, NotAuthor, ChatNotFound, PermissionDenied
from errors import InternalError, UserNotFound, UserAlreadyInChat, CantInvitePrivateChat
import logging


logger = logging.getLogger(__name__)


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
            headers={
                "X-User-Id": user_id
            },
            json={
                "chat_id": payload.get("chat_id"),
                "reply_to_message_id": payload.get("reply_to_message_id"),
                "data_type": "TextOrAttachments",
                "body": payload.get("body"),
            })

        if response.status_code == 403:
            raise NotInChat
        elif response.is_success:
            return response.json()
        else:
            raise ChatServiceUnavailable

    async def delete_message(self, user_id: str, payload: dict):
        response = await self._make_request(
            method="DELETE",
            url=f"/api/messages/{payload.get("message_id")}",
            headers={
                "X-User-Id": user_id
            })
        if response.status_code == 404:
            raise MessageNotFound
        elif response.status_code == 403:
            raise PermissionDenied
        elif response.is_success:
            return response.json()
        else:
            raise ChatServiceUnavailable

    async def edit_message(self, user_id: str, payload: dict):
        response = await self._make_request(
            method="PATCH",
            url=f"/api/messages/{payload.get("message_id")}",
            headers={
                "X-User-Id": user_id
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

    async def get_chat_members(self, chat_id: int):
        response = await self._make_request(
            method="GET",
            url=f"/api/chats/{chat_id}/members",
        )
        if response.status_code == 404:
            raise ChatNotFound
        if response.is_success:
            return response.json()
        else:
            raise ChatServiceUnavailable

    async def create_chat(self, user_id: str, payload: dict):
        response = await self._make_request(
            method="POST",
            url="/api/chats",
            headers={
                "X-User-Id": user_id
            },
            json={
                "type": payload.get("type"),
                "title": payload.get("title"),
                "pfp_media_url": payload.get("pfp_media_url"),
                "members": payload.get("members")
            }
        )
        if response.status_code == 422:
            logger.error("рассогласование в схемах между chat_service и gateway, %s", response.text)
            raise InternalError
        if response.status_code == 400:
            raise UserNotFound
        if response.is_success:
            return response.json()
        else:
            raise ChatServiceUnavailable

    async def get_chat_messages(self, user_id: str, chat_id: int, cursor: int | None, per_page: int):
        params = {"per_page": per_page}
        if cursor is not None:
            params["cursor"] = cursor

        response = await self._make_request(
            method="GET",
            url=f"/api/chats/{chat_id}/messages",
            headers={
                "X-User-Id": user_id
            },
            params=params
        )
        if response.is_success:
            return response.json()
        if response.status_code == 404:
            raise ChatNotFound
        if response.status_code == 403:
            raise PermissionDenied
        else:
            raise ChatServiceUnavailable

    async def get_user_chats(self, user_id: str, cursor: int | None, per_page: int):
        params = {"per_page": per_page}
        if cursor is not None:
            params["cursor"] = cursor

        response = await self._make_request(
            method="GET",
            url=f"/api/users/{user_id}/chats",
            params=params
        )

        if response.is_success:
            return response.json()
        if response.status_code == 404:
            raise UserNotFound
        else:
            raise ChatServiceUnavailable

    async def user_leave_chat(self, user_id: str, payload: dict):
        response = await self._make_request(
            method="DELETE",
            url=f"/api/chats/{payload["chat_id"]}/members/{user_id}/",
            headers={
                "X-User-Id": user_id
            },
            json={
                "chat_id": payload["chat_id"]
            }
        )
        if response.is_success:
            return
        if response.status_code == 404:
            raise ChatNotFound
        if response.status_code == 403:
            raise NotInChat
        else:
            raise ChatServiceUnavailable

    async def add_user_to_chat(self, user_id: str, payload: dict):
        response = await self._make_request(
            method="POST",
            url=f"/api/chats/{payload["chat_id"]}/members/",
            headers={
                "X-User-Id": user_id
            },
            json={
                "chat_id": payload["chat_id"],
                "user_id": payload["target_id"]
            }
        )

        if response.is_success:
            return response.json()
        if response.status_code == 404:
            raise UserNotFound
        if response.status_code == 422:
            raise CantInvitePrivateChat
        if response.status_code == 409:
            raise UserAlreadyInChat
        else:
            raise ChatServiceUnavailable
