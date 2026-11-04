class GatewayError(Exception):
    pass


class FatalError(GatewayError):
    code = "internal_error"
    close_code = 1011
    http_status = 500


class CommandError(GatewayError):
    pass


class InvalidTicket(FatalError):
    code = "invalid_ticket"
    close_code = 1008
    http_status = 401


class InvalidToken(FatalError):
    code = "invalid_token"
    close_code = 1008
    http_status = 401


class AuthServiceUnavailable(FatalError):
    code = "auth_service_unavailable"
    close_code = 1013
    http_status = 503


class TicketStoreUnavailable(FatalError):
    code = "ticket_store_unavailable"
    close_code = 1013
    http_status = 503


class UserNotFoundAuthService(FatalError):
    code = "user_not_found_auth_service"
    close_code = 1008
    http_status = 401

class NotAuthor(CommandError):
    code = "user_not_author"


class MessageNotFound(CommandError):
    code = "message_not_found"


class UnknownCommand(CommandError):
    code = "unknown_command"


class InvalidPayload(CommandError):
    code = "invalid_payload"


class ChatServiceUnavailable(CommandError):
    code = "chat_service_unavailable"


class ChatNotFound(CommandError):
    code = "chat_not_found"


class UserNotFound(CommandError):
    code = "user_not_found"


class NotInChat(CommandError):
    code = "user_not_in_chat"


class InternalError(CommandError):
    code = "internal_error"


class PermissionDenied(CommandError):
    code = "permission_denied"
