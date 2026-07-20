class UserHandler:
    def __init__(self, connection_manager, message_client, chat_client):
        self.connection_manager = connection_manager
        self.message_client = message_client
        self.chat_client = chat_client

    async def typing(self, username: str, data: dict):
        pass
