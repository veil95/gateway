from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from Clients.Auth_Client import get_current_user
from model.Exceptions import AuthError
from dependencies import connection_manager, dispatcher


router = APIRouter(tags=["webscokets"])


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
    connection_manager.connect(username=username, websocket=websocket)
    while True:
        try:
            data = await websocket.receive_json()
        except WebSocketDisconnect:
            connection_manager.disconnect(username, websocket)
            return
        await dispatcher.handle(username, data)


    