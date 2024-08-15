from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.log_active_connections("Client connected")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.log_active_connections("Client disconnected")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        connections_count = len(self.active_connections)
        print(f"Broadcasting message to {connections_count} clients")
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))
        print(f"Message sent to {connections_count} clients")

    def log_active_connections(self, action):
        print(f"{action}. Total active connections: {len(self.active_connections)}")

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get('message') == 'Emergencia':
                print("Received an emergency message.")
                await manager.broadcast({"type": "emergency", "message": "Emergencia"})
            else:
                await manager.broadcast({"type": "alert", "message": message})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"type": "info", "message": "A client left the chat"})
