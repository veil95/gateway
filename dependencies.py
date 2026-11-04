from typing import Annotated
from fastapi import Request
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from services.connection_manager import ConnectionManager
from clients.auth_client import AuthClient
from services.dispatcher import Dispatcher
from services.ticket_store import TicketStore


def get_auth_client(request: Request) -> AuthClient:
    return request.app.state.auth_client


def get_connection_manager(request: Request) -> ConnectionManager:
    return request.app.state.connection_manager


def get_dispatcher(request: Request) -> Dispatcher:
    return request.app.state.dispatcher


def get_ticket_store(request: Request) -> TicketStore:
    return request.app.state.ticket_store


security = HTTPBearer()


AuthClientDep = Annotated[AuthClient, Depends(get_auth_client)]
ConnectionManagerDep = Annotated[ConnectionManager, Depends(get_connection_manager)]
TicketStoreDep = Annotated[TicketStore, Depends(get_ticket_store)]
DispatcherDep = Annotated[Dispatcher, Depends(get_dispatcher)]
HTTPBearerDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]