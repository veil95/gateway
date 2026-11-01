from typing import Optional
from uuid import UUID

from schemas.command_type import CommandType
from pydantic import BaseModel, Field, model_validator, field_validator
from schemas.command_type import ChatType
from errors import InvalidPayload
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


class CreateChatPayload(BaseModel):
    type: ChatType
    title: str | None = Field(min_length=1, max_length=128, default=None)
    pfp_media_url: Optional[str] = Field(default=None, max_length=255)
    members: list[UUID]

    @model_validator(mode="after")
    def type_members_check(self):
        if self.type == ChatType.DIRECT:
            if len(self.members) != 1:
                raise ValueError("Кол-во участников при type == Direct должно быть равно 1")
            if self.title is not None:
                raise ValueError("При type == direct не может быть title")
        if self.type == ChatType.GROUP:
            if len(self.members) < 1:
                raise ValueError("при type == group, members >= 1")
            if self.title is None:
                raise ValueError("при type == group, title не может быть None")
        return self

    @field_validator("members")
    @classmethod
    def check_duplicates(cls, value: list):
        if len(set(value)) != len(value):
            raise ValueError("дубликаты в members, нельзя добавить одного участника дважды")
        return value


PAYLOAD_SCHEMAS = {
    CommandType.SEND_MESSAGE: SendMessagePayload,
    CommandType.TYPING: TypingPayload,
    CommandType.DELETE_MESSAGE: DeleteMessagePayload,
    CommandType.EDIT_MESSAGE: EditMessagePayload,
    CommandType.CREATE_CHAT: CreateChatPayload
}
