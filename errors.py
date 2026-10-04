class GatewayError(Exception):
    pass


class FatalError(GatewayError):
    pass


class CommandError(GatewayError):
    pass


class InvalidTicket(FatalError):
    close_code = 1008


class InvalidToken(FatalError):
    close_code = 1008


class AuthServiceUnavailable(FatalError):
    close_code = 1013


class UserNotFoundAuthService(FatalError):
    close_code = 1008


class UnknownCommand(CommandError):
    code = "unknown_command"


class InvalidPayload(CommandError):
    code = "invalid_payload"


class ChatServiceUnavailable(CommandError):
    code = "chat_service_unavailable"


class UserNotFound(CommandError):
    code = "user_not_found"


class NotInChat(CommandError):
    code = "user_not_in_chat"
