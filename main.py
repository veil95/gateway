from os import getenv
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from view.ws import router
from contextlib import asynccontextmanager
from clients.auth_client import AuthClient
from clients.chat_client import ChatClient
from config import chat_service_url, auth_service_url


@asynccontextmanager
async def lifespan(app: FastAPI):
    http_auth = httpx.AsyncClient(base_url=auth_service_url, timeout=5)
    http_chat = httpx.AsyncClient(base_url=chat_service_url, timeout=5)
    app.state.chat_client = ChatClient(http_chat)
    app.state.auth_client = AuthClient(http_auth)
    yield
    await http_auth.aclose()
    await http_chat.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
async def get():
    return {"status": "ok"}
