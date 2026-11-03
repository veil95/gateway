from clients.chat_client import ChatClient
from services.chat_broadcaster import Broadcast
from services.connection_manager import ConnectionManager
from schemas.events import Event

class UserHandler:
    def __init__(self, connection_manager: ConnectionManager, chat_client: ChatClient, broadcaster: Broadcast):
        self.connection_manager = connection_manager
        self.chat_client = chat_client
        self.broadcaster = broadcaster

    async def typing(self, user_id: str, payload: dict):
        message_for_front = {"chat_id": payload["chat_id"],
                             "user_id": user_id}
        event = Event(type="typing", payload=message_for_front)
        offline_users = await self.broadcaster.broadcast_check_author(user_id=user_id, event=event, chat_id=payload["chat_id"])
        return None