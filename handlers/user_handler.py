from clients.chat_client import ChatClient
from services.chat_broadcaster import Broadcast
from services.connection_manager import ConnectionManager


class UserHandler:
    def __init__(self, connection_manager: ConnectionManager, chat_client: ChatClient, broadcaster: Broadcast):
        self.connection_manager = connection_manager
        self.chat_client = chat_client
        self.broadcaster = broadcaster

    async def typing(self, user_id: str, payload: dict):
        ...
