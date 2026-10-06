from clients.chat_client import ChatClient

class ChatHandler:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    async def create_chat(self, user_id: str, data: dict, chat_client: ChatClient):
        pass

    async def add_user(self, user_id: str, data: dict, chat_client: ChatClient):
        pass

    async def kick_user(self, user_id: str, data: dict, chat_client: ChatClient):
        pass

    async def leave_chat(self, user_id: str, data: dict, chat_client: ChatClient):
        pass
