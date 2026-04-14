from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

import logging
logger = logging.getLogger(__name__)
router = APIRouter()

# Keep track of active WebSocket connections
class ConnectionManager:
    def __init__(self):
        # We might have one ESP32 sending data, and multiple Frontend clients receiving it
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WS connection: {websocket.client.host}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        logger.debug(f"Broadcasting data to {len(self.active_connections)} clients: {message[:100]}...")
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                logger.warning("Failed to send to client, removing")
                pass

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_live_feed(websocket: WebSocket):
    """
    WebSocket endpoint for both ESP32 (producer) and React frontend (consumer).
    When ESP32 sends JSON data, it broadcasts to all connected clients.
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received WS data from {websocket.client.host}: {data[:100]}...")
            await manager.broadcast(data)
    except WebSocketDisconnect:
        logger.info(f"WS client disconnected: {websocket.client.host}")
        manager.disconnect(websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
