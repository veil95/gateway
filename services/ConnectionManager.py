from typing import Dict
from fastapi import WebSocket


class ConnectionManager():
    def __init__(self):
        self.active_connections: Dict[str, list[WebSocket]] = {}
    async def connect(self, username, websocket: WebSocket):
        if username not in self.active_connections:
            self.active_connections[username] = [websocket]
        else:
            self.active_connections[username].append(websocket)
    async def disconnect(self, username, websocket: WebSocket):
        if username in self.active_connections:
            try:
                self.active_connections[username].remove(websocket)
                if not self.active_connections[username]:
                    del self.active_connections[username]
            except ValueError:
                print(f"WebSocket not found for user {username}")
    async def send_to_user(self, receiver: str, data: dict) -> bool:
        connections = self.active_connections.get(receiver)
        if not connections:
            return False
        for websocket in connections:
            await websocket.send_json(data)
        return True

