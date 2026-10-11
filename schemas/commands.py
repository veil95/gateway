from typing import Optional
from schemas.command_type import CommandType
from pydantic import BaseModel, Field


class Envelope(BaseModel):
    type: str
    request_id: str
    payload: dict


class SendMessagePayload(BaseModel):
    chat_id: int
    body: str = Field(min_length=1, max_length=4000)
    reply_to_message_id: Optional[int] = None


class TypingPayload(BaseModel):
    chat_id: int


class EditMessagePayload(BaseModel):
    message_id: int
    body: str = Field(min_length=1, max_length=4000)


class DeleteMessagePayload(BaseModel):
    message_id: int


PAYLOAD_SCHEMAS = {
    CommandType.SEND_MESSAGE: SendMessagePayload,
    CommandType.TYPING: TypingPayload,
    CommandType.DELETE_MESSAGE: DeleteMessagePayload,
    CommandType.EDIT_MESSAGE: EditMessagePayload
}