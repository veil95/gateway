from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, set[WebSocket]] = dict()

    def connect(self, username: str, websocket: WebSocket):
        if username not in self.active_connections:
            self.active_connections[username] = {websocket}
        else:
            self.active_connections[username].add(websocket)

    def disconnect(self, username: str, websocket: WebSocket):
        if username not in self.active_connections:
            return
        self.active_connections[username].discard(websocket)
        if not self.active_connections[username]:
            self.active_connections.pop(username)

    async def send_to_user(self, receiver: str, data: dict) -> bool:
        connections = self.active_connections.get(receiver)
        if not connections:
            return False
        for websocket in connections.copy():
            try:
                await websocket.send_json(data)
            except (WebSocketDisconnect, ConnectionClosedOK, ConnectionClosedError):
                self.disconnect(receiver, websocket)
        return True

