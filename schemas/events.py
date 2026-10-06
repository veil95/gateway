from typing import Optional

from pydantic import BaseModel


class ErrorBody(BaseModel):
    code: str
    message: str


class Response(BaseModel):
    type: str
    request_id: str
    payload: dict


class ErrorResponse(BaseModel):
    type: str = "error"
    request_id: str
    error: ErrorBody


class Event(BaseModel):
    type: str
    payload: dict