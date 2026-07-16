from fastapi import FastAPI, WebSocket, APIRouter, WebSocketDisconnect
from services.ConnectionManager import ConnectionManager
from services.Auth_Client import get_current_user
from model.Exceptions import AuthError

router = APIRouter(tags=["webscokets"])

connectionmanager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.cookies.get("access_token")
    if not token:
        await websocket.close(code=1008)
        return
    try:
        user = await get_current_user(token)
    except AuthError:
        await websocket.close(code=1008)
        return
    username = user.get("username")
    await websocket.accept()
    connectionmanager.connect(username=username, websocket=websocket)
    while True:
        try:
            data = await websocket.receive_json()
        except WebSocketDisconnect:
            connectionmanager.disconnect(username, websocket)
            return
        await websocket.send_json(data)


    