import httpx
from fastapi import FastAPI
from view.ws import router
from view.ws_tickets import ticket_router
from view.auth import auth_router
from contextlib import asynccontextmanager
from clients.auth_client import AuthClient
from clients.chat_client import ChatClient
from config import chat_service_url, auth_service_url, redis_url
from services.dispatcher import Dispatcher
from services.connection_manager import ConnectionManager
from services.chat_broadcaster import Broadcast
from redis.asyncio import Redis
import logging
from services.ticket_store import TicketStore
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s | %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    http_chat = httpx.AsyncClient(base_url=chat_service_url, timeout=5)
    redis = Redis.from_url(redis_url, decode_responses=True)
    chat_client = ChatClient(http_chat)
    auth_client = AuthClient(base_url=auth_service_url, timeout=5)
    connection_manager = ConnectionManager()
    broadcaster = Broadcast(connection_manager=connection_manager, chat_client=chat_client)
    dispatcher = Dispatcher(connection_manager=connection_manager, chat_client=chat_client, broadcaster=broadcaster)
    ticket_store = TicketStore(redis)

    app.state.chat_client = chat_client
    app.state.auth_client = auth_client
    app.state.broadcaster = broadcaster
    app.state.dispatcher = dispatcher
    app.state.connection_manager = connection_manager
    app.state.ticket_store = ticket_store

    yield

    await http_chat.aclose()
    await redis.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.include_router(ticket_router)
app.include_router(auth_router)


@app.get("/")
async def get():
    return {"status": "ok"}
