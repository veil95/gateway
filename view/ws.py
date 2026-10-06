from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from errors import AuthServiceUnavailable
from dependencies import AuthClientDep

router = APIRouter(tags=["websockets"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, auth_service: AuthClientDep):
    token = websocket.cookies.get("access_token")
    if not token:
        await websocket.close(code=1008)
        return
    try:
        user = await auth_service.get_current_user(token)
    except AuthServiceUnavailable:
        await websocket.close(code=1008)
        return
    user_id = user.get("user_id")
    await websocket.accept()
    connection_manager.connect(usser_id=user_id, websocket=websocket)
    while True:
        try:
            data = await websocket.receive_json()
        except WebSocketDisconnect:
            connection_manager.disconnect(user_id, websocket)
            return
        await dispatcher.handle(user_id, data)


    