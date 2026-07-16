from typing import Dict
from httpx import AsyncClient
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from services.ConnectionManager import ConnectionManager
from view.ws import router


app = FastAPI()
app.include_router(router)


@app.get("/")
async def get():
    return
