from clients.chat_client import ChatClient


class UserHandler:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    async def typing(self, username: str, data: dict, chat_client: ChatClient):
        ...
