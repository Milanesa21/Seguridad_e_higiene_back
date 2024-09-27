
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, id_empresa: str):
        await websocket.accept()
        if id_empresa not in self.active_connections:
            self.active_connections[id_empresa] = []
        self.active_connections[id_empresa].append(websocket)
        self.log_active_connections("Client connected", id_empresa)

    def disconnect(self, websocket: WebSocket, id_empresa: str):
        self.active_connections[id_empresa].remove(websocket)
        if not self.active_connections[id_empresa]:
            del self.active_connections[id_empresa]
        self.log_active_connections("Client disconnected", id_empresa)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict, id_empresa: str):
        if id_empresa in self.active_connections:
            connections_count = len(self.active_connections[id_empresa])
            print(f"Broadcasting message to {connections_count} clients of empresa {id_empresa}")
            for connection in self.active_connections[id_empresa]:
                await connection.send_text(json.dumps(message))
            print(f"Message sent to {connections_count} clients of empresa {id_empresa}")

    def log_active_connections(self, action: str, id_empresa: str):
        connections_count = len(self.active_connections.get(id_empresa, []))
        print(f"{action} for empresa {id_empresa}. Total active connections: {connections_count}")

manager = ConnectionManager()

@router.websocket("/ws/{id_empresa}")
async def websocket_endpoint(websocket: WebSocket, id_empresa: str):
    if not id_empresa or id_empresa == "null":
        # Si id_empresa no está presente, lo tratamos como el id del usuario
        id_empresa = websocket.headers.get("id")
        if not id_empresa:
            await websocket.close()
            return

    await manager.connect(websocket, id_empresa)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get('message') == 'Emergencia':
                print(f"Received an emergency message for empresa {id_empresa}.")
                await manager.broadcast({"type": "emergency", "message": "Emergencia"}, id_empresa)
            else:
                await manager.broadcast({"type": "alert", "message": message}, id_empresa)
    except WebSocketDisconnect:
        manager.disconnect(websocket, id_empresa)
        await manager.broadcast({"type": "info", "message": "A client left the chat"}, id_empresa)
