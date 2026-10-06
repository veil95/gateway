from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, set[WebSocket]] = dict()

    def connect(self, user_id: str, websocket: WebSocket):
        if user_id not in self.active_connections:
            self.active_connections[user_id] = {websocket}
        else:
            self.active_connections[user_id].add(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        if user_id not in self.active_connections:
            return
        self.active_connections[user_id].discard(websocket)
        if not self.active_connections[user_id]:
            self.active_connections.pop(user_id)

    async def _send_to_one(self, user_id: str, data: dict) -> str | None:
        connections = self.active_connections.get(user_id)
        if not connections:
            return user_id
        for websocket in connections.copy():
            try:
                await websocket.send_json(data)
            except (WebSocketDisconnect, ConnectionClosedOK, ConnectionClosedError):
                self.disconnect(user_id, websocket)
        return None

    async def send_to_users(self, user_ids: list[str], data: dict):
        offline_users = set()
        for user in user_ids:
            user_id = await self._send_to_one(user_id=user, data=data)
            if user_id:
                offline_users.add(user_id)
        return offline_users
