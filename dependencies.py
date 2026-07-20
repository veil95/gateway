from services.ConnectionManager import ConnectionManager
from Clients.Message_Client import MessageClient
from Clients.Chat_Client import ChatClient
from services.dispatcher import Dispatcher

# Shared instances
connection_manager = ConnectionManager()

message_client = MessageClient("url")
chat_client = ChatClient("url")

dispatcher = Dispatcher(connection_manager=connection_manager,
                        message_client=message_client,
                        chat_client=chat_client)
