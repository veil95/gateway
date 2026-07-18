from enum import Enum


class CommandType(str, Enum):
    SEND_MESSAGE = "send_message"
    TYPING = "typing"
    GET_CHAT_HISTORY = "get_chat_history"
    CREATE_CHAT = "create_chat"
    EDIT_MESSAGE = "edit_message"
    DELETE_MESSAGE = "delete_message"
    ADD_USER_TO_CHAT = "add_user_to_chat"
    LEAVE_CHAT = "leave_chat"
    MARK_AS_READ = "mark_as_read"
    PING = "ping"
