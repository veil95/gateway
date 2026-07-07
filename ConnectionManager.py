from typing import Dict
from fastapi import WebSocket


class ConnectionManager():
    def __init__(self):
        self.active_connections: Dict[int, list(WebSocket)] = {}
    def connect(self, user_id, websocket: WebSocket):
        if user_id not in self.active_connections:
            self.active_connections[user_id] = [websocket]
        else:
            self.active_connections[user_id].append(websocket)
    def disconnect(self, user_id, websocket: WebSocket):
        if user_id in self.active_connections:
            try:
                self.active_connections[user_id].remove(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            except ValueError:
                print(f"WebSocket not found for user {user_id}")