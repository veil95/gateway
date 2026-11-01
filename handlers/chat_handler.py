from clients.chat_client import ChatClient
from services.chat_broadcaster import Broadcast
from services.connection_manager import ConnectionManager
from schemas.events import Event


class ChatHandler:
    def __init__(self, connection_manager: ConnectionManager, chat_client: ChatClient, broadcaster: Broadcast):
        self.connection_manager = connection_manager
        self.chat_client = chat_client
        self.broadcaster = broadcaster

    async def create_chat(self, user_id: str, payload: dict):
        response = await self.chat_client.create_chat(user_id=user_id, payload=payload)
        message = response
        event = Event(type="chat_created", payload=message)
        offline_users = await self.broadcaster.broadcast_to_members(user_id=user_id,
                                                                    event=event,
                                                                    members=payload["members"])
        return {"type": "chat_created_confirmed", "payload": message}

    async def add_user(self, user_id: str, payload: dict):
        pass

    async def kick_user(self, user_id: str, payload: dict):
        pass

    async def leave_chat(self, user_id: str, payload: dict):
        pass
