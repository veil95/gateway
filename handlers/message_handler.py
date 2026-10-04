from clients.chat_client import ChatClient


class MessageHandler:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    async def send_message(self, username: str, data: dict, chat_client: ChatClient):
        ...

    async def edit_message(self, username: str, data: dict, chat_client: ChatClient):
        ...

    async def delete_message(self, username: str, data: dict, chat_client: ChatClient):
        ...
