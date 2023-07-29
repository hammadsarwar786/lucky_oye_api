from fastapi import FastAPI, WebSocket, APIRouter, HTTPException, Request, Depends
import psycopg2
from database import get_database_connection
from typing import List
import asyncio

# WebSocket manager to handle connected clients
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_notification(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def emit_to_client(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

websocket_manager = WebSocketManager()
router = APIRouter()

@router.post("/notification")
async def create_notification(message: Request, db: psycopg2.extensions.connection = Depends(get_database_connection)):
    try:
        data = await message.json()
        cursor = db.cursor()
        # Replace 'notification' with your actual table name and 'message' with the appropriate column name
        cursor.execute("INSERT INTO notification (message) VALUES (%s)", (data["message"],))
        db.commit()
        cursor.close()

        # Send the new notification to all connected WebSocket clients
        await websocket_manager.broadcast_notification(message=data["message"])
        return {"success": True, "message": "Notification created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating notification: {str(e)}")


@router.websocket("socket/notification")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Send a response back to the client
            await websocket_manager.emit_to_client(websocket, f"Received: {data}")
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        websocket_manager.disconnect(websocket)