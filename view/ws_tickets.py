
from fastapi import APIRouter


ticket_router = APIRouter(tags=["ticket"])

@ticket_router.post("/ws-ticket")
async def tickets():
    pass
