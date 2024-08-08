import socket
import socketio
from fastapi import FastAPI
from fastapi_socketio import SocketManager

sio = socketio.AsyncServer()
app = FastAPI()
socket_manager = SocketManager(app=app, socketio_server=sio)

@sio.event
async def connect(sid, environ):
    print(f"connect {sid}")

@sio.event
async def disconnect(sid):
    print(f"disconnect {sid}")

@sio.event
async def sed_alert(sid,data):
    print(f"Alerta recibida de {sid}: {data}")

    await sio.emit('alert',data)