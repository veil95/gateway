from typing import Annotated
from fastapi import Request
from fastapi import Depends
from services.connection_manager import ConnectionManager
from clients.auth_client import AuthClient
from clients.chat_client import ChatClient
from services.dispatcher import Dispatcher


def get_auth_client(request: Request) -> AuthClient:
    return request.app.state.auth_client


def get_chat_client(request: Request) -> ChatClient:
    return request.app.state.chat_client


def get_connection_manager(request: Request) -> ConnectionManager:
    return request.app.state.connection_manager


def get_dispatcher(request: Request) -> Dispatcher:
    return request.app.state.dispatcher


ChatClientDep = Annotated[ChatClient, Depends(get_chat_client)]
AuthClientDep = Annotated[AuthClient, Depends(get_auth_client)]

ConnectionManagerDep = Annotated[ConnectionManager, Depends(get_connection_manager)]

DispatcherDep = Annotated[Dispatcher, Depends(get_dispatcher)]