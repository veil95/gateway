from model.Command_Type import CommandType
from model.Exceptions import UnknownCommand
from handlers.Chat_Handler import ChatHandler
from handlers.User_Handler import UserHandler
from handlers.Message_Handler import MessageHandler


class Dispatcher:
    def __init__(self, connection_manager, message_client, chat_client):
        self.message_handler = MessageHandler(connection_manager=connection_manager,
                                              message_client=message_client,
                                              chat_client=chat_client)
        self.user_handler = UserHandler(connection_manager=connection_manager,
                                        message_client=message_client,
                                        chat_client=chat_client)
        self.chat_handler = ChatHandler(connection_manager=connection_manager,
                                        message_client=message_client,
                                        chat_client=chat_client)

        self.commands = {
            CommandType.SEND_MESSAGE: self.message_handler.send_message,
            CommandType.EDIT_MESSAGE: self.message_handler.edit_message,
            CommandType.DELETE_MESSAGE: self.message_handler.delete_message,

            CommandType.CREATE_CHAT: self.chat_handler.create_chat,
            CommandType.LEAVE_CHAT: self.chat_handler.leave_chat,
            CommandType.ADD_USER_TO_CHAT: self.chat_handler.add_user,
            CommandType.KICK_USER_FROM_CHAT: self.chat_handler.kick_user,

            CommandType.TYPING: self.user_handler.typing,
        }

    async def handle(self, username: str, data: dict):
        command = data.get("type")
        if command is None:
            raise UnknownCommand()

        try:
            command = CommandType(command)
        except ValueError:
            raise UnknownCommand()

        handler = self.commands.get(command)
        if handler is None:
            raise UnknownCommand()

        await handler(username, data)
