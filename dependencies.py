from typing import Annotated
from fastapi import Request
from fastapi import Depends
from services.connection_manager import ConnectionManager
from clients.auth_client import AuthClient
from clients.chat_client import ChatClient
from services.dispatcher import Dispatcher
# Shared instances


def get_auth_service(request: Request) -> AuthClient:
    return request.app.state.auth_client


def get_chat_service(request: Request) -> ChatClient:
    return request.app.state.chat_client


ChatClientDep = Annotated[ChatClient, Depends(get_chat_service)]
AuthClientDep = Annotated[AuthClient, Depends(get_auth_service)]

connection_manager = ConnectionManager()

dispatcher = Dispatcher(connection_manager=connection_manager)
