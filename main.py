import httpx
from fastapi import FastAPI
from view.ws import router
from contextlib import asynccontextmanager
from clients.auth_client import AuthClient
from clients.chat_client import ChatClient
from config import chat_service_url, auth_service_url
from services.dispatcher import Dispatcher
from services.connection_manager import ConnectionManager
from services.chat_broadcaster import Broadcast

@asynccontextmanager
async def lifespan(app: FastAPI):
    http_auth = httpx.AsyncClient(base_url=auth_service_url, timeout=5)
    http_chat = httpx.AsyncClient(base_url=chat_service_url, timeout=5)
    chat_client = ChatClient(http_chat)
    app.state.chat_client = chat_client
    app.state.auth_client = AuthClient(http_auth)
    connection_manager = ConnectionManager()
    broadcaster = Broadcast(connection_manager=connection_manager, chat_client=chat_client)
    dispatcher = Dispatcher(connection_manager=connection_manager, chat_client=chat_client, broadcaster=broadcaster)
    app.state.broadcaster = broadcaster
    app.state.dispatcher = dispatcher
    app.state.connection_manager = connection_manager
    yield
    await http_auth.aclose()
    await http_chat.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
async def get():
    return {"status": "ok"}
