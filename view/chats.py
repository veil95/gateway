from dependencies import HTTPBearerDep, ChatClientDep, AuthClientDep
from fastapi import APIRouter, Request, HTTPException
from errors import FatalError, ChatServiceUnavailable, CommandError
from schemas.commands import GetChatMessagesPayload, PaginationPayload
from pydantic import ValidationError


chat_router = APIRouter(tags=["chat_service"])


@chat_router.get("/chats/{chat_id}/messages")
async def get_chat_messages(credentials: HTTPBearerDep, request: Request, chat_id: int, auth_service: AuthClientDep,
                            chat_service: ChatClientDep):
    q_params = request.query_params
    pagination = {}
    for key in ["cursor", "per_page"]:
        if key in q_params:
            pagination[key] = q_params[key]
    token = credentials.credentials
    try:
        user = await auth_service.get_current_user(token=token)
    except FatalError as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.code)

    try:
        payload = GetChatMessagesPayload(chat_id=chat_id, **pagination)
    except ValidationError:
        raise HTTPException(status_code=422, detail="invalid_payload")
    try:
        response = await chat_service.get_chat_messages(user_id=user["user_id"], chat_id=payload.chat_id,
                                                    cursor=payload.cursor, per_page=payload.per_page)
    except CommandError as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.code)

    return response


@chat_router.get("/chats")
async def get_user_chats(credentials: HTTPBearerDep, request: Request,
                         auth_service: AuthClientDep, chat_service: ChatClientDep):
    q_params = request.query_params
    pagination = {}
    for key in ["cursor", "per_page"]:
        if key in q_params:
            pagination[key] = q_params[key]

    token = credentials.credentials

    try:
        user = await auth_service.get_current_user(token)
    except FatalError as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.code)

    try:
        payload = PaginationPayload(**pagination)
    except ValidationError:
        raise HTTPException(status_code=422, detail="invalid_payload")

    try:
        response = await chat_service.get_user_chats(user_id=user["user_id"], cursor=payload.cursor,
                                                     per_page=payload.per_page)
    except CommandError as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.code)

    return response
