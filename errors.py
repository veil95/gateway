class GatewayError(Exception):
    pass


class FatalError(GatewayError):
    code = "internal_error"
    close_code = 1011
    http_status = 500


class CommandError(GatewayError):
    http_status = 500


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


class IncorrectCredential(CommandError):
    code = "incorrect_login_or_password"


class CantInvitePrivateChat(CommandError):
    code = "cant_invite_to_private_chat"
    http_status = 422


class UserAlreadyInChat(CommandError):
    code = "user_already_in_chat"
    http_status = 409


class NotAuthor(CommandError):
    code = "user_not_author"


class MessageNotFound(CommandError):
    code = "message_not_found"


class UnknownCommand(CommandError):
    code = "unknown_command"


class InvalidPayload(CommandError):
    code = "invalid_payload"


class ChatServiceUnavailable(CommandError):
    http_status = 503
    code = "chat_service_unavailable"


class ChatNotFound(CommandError):
    http_status = 404
    code = "chat_not_found"


class UserNotFound(CommandError):
    http_status = 404
    code = "user_not_found"


class NotInChat(CommandError):
    code = "user_not_in_chat"


class InternalError(CommandError):
    code = "internal_error"


class PermissionDenied(CommandError):
    http_status = 403
    code = "permission_denied"
