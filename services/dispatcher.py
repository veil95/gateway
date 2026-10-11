from pydantic import ValidationError

from schemas.command_type import CommandType
from errors import UnknownCommand, InvalidPayload
from handlers.chat_handler import ChatHandler
from handlers.user_handler import UserHandler
from handlers.message_handler import MessageHandler
from clients.chat_client import ChatClient
from schemas.events import ErrorResponse
from schemas.commands import PAYLOAD_SCHEMAS
from schemas.commands import Envelope

class Dispatcher:
    def __init__(self, connection_manager):
        self.message_handler = MessageHandler(connection_manager=connection_manager)
        self.user_handler = UserHandler(connection_manager=connection_manager)
        self.chat_handler = ChatHandler(connection_manager=connection_manager)

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

    async def handle(self, user_id: str, envelope: Envelope, chat_client: ChatClient):
        command = envelope.type
        try:
            command = CommandType(command)
        except ValueError:
            raise UnknownCommand()
        try:
            schema = PAYLOAD_SCHEMAS[command]
        except KeyError:
            raise UnknownCommand
        try:
            payload = schema(**envelope.payload)
        except ValidationError as e:
            raise InvalidPayload
        handler = self.commands.get(command)
        if handler is None:
            raise UnknownCommand()
        return await handler(user_id=user_id, payload=payload.model_dump(), chat_client=chat_client)
