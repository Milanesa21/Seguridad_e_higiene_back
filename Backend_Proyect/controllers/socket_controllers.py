from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import List
import json
from model.alert_message import AlertMessage
from model.schemas.alert_message_schemas import AlertMessageRequest
from dataBase.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast al resto de conexiones
            await manager.broadcast({"message": f"New alert: {data}"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"message": "A client left the chat"})


@router.post('/alert/sendMessage')
async def send_message(alert_message: AlertMessageRequest, db: Session = Depends(get_db)):
    full_name = alert_message.full_name
    user_id = alert_message.user_id
    puesto_trabajo = alert_message.puesto_trabajo
    message = alert_message.message

    if not message:
        message = "¡Emergencia! Necesito asistencia."
    
    alert_message_instance = AlertMessage(user_id=user_id, full_name=full_name, puesto_trabajo=puesto_trabajo, message=message)
    db.add(alert_message_instance)
    db.commit()

    # Enviar mensaje a todos los clientes conectados a través del WebSocket
    message_data = {"user_id": user_id, "full_name": full_name, "puesto_trabajo": puesto_trabajo, "message": message}
    await manager.broadcast(message_data)

    return {"message": f"Mensaje enviado de {full_name} en el puesto de trabajo {puesto_trabajo}: {message}"}
