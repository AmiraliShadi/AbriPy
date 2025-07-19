# http/websockets.py
import asyncio
import json
from typing import Dict, List, Callable, Any, Optional
import uuid

class WebSocketConnection:
    """WebSocket connection wrapper"""
    
    def __init__(self, websocket, connection_id: str = None):
        self.websocket = websocket
        self.connection_id = connection_id or str(uuid.uuid4())
        self.is_connected = True
        self.user_data: Dict[str, Any] = {}
    
    async def send_text(self, message: str):
        """Send text message"""
        if self.is_connected:
            try:
                await self.websocket.send_text(message)
            except Exception:
                self.is_connected = False
    
    async def send_json(self, data: Dict[str, Any]):
        """Send JSON message"""
        await self.send_text(json.dumps(data))
    
    async def receive_text(self) -> str:
        """Receive text message"""
        return await self.websocket.receive_text()
    
    async def receive_json(self) -> Dict[str, Any]:
        """Receive JSON message"""
        text = await self.receive_text()
        return json.loads(text)
    
    async def close(self):
        """Close connection"""
        self.is_connected = False
        await self.websocket.close()

class WebSocketManager:
    """WebSocket connection manager"""
    
    def __init__(self):
        self.connections: Dict[str, WebSocketConnection] = {}
        self.rooms: Dict[str, List[str]] = {}
        self.handlers: Dict[str, Callable] = {}
    
    def add_connection(self, connection: WebSocketConnection):
        """Add new connection"""
        self.connections[connection.connection_id] = connection
    
    def remove_connection(self, connection_id: str):
        """Remove connection"""
        if connection_id in self.connections:
            # Remove from all rooms
            for room_connections in self.rooms.values():
                if connection_id in room_connections:
                    room_connections.remove(connection_id)
            
            del self.connections[connection_id]
    
    def join_room(self, connection_id: str, room_name: str):
        """Add connection to room"""
        if room_name not in self.rooms:
            self.rooms[room_name] = []
        
        if connection_id not in self.rooms[room_name]:
            self.rooms[room_name].append(connection_id)
    
    def leave_room(self, connection_id: str, room_name: str):
        """Remove connection from room"""
        if room_name in self.rooms and connection_id in self.rooms[room_name]:
            self.rooms[room_name].remove(connection_id)
    
    async def broadcast_to_room(self, room_name: str, message: Dict[str, Any]):
        """Broadcast message to all connections in room"""
        if room_name not in self.rooms:
            return
        
        disconnected = []
        
        for connection_id in self.rooms[room_name]:
            if connection_id in self.connections:
                connection = self.connections[connection_id]
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection_id)
        
        # Clean up disconnected connections
        for connection_id in disconnected:
            self.remove_connection(connection_id)
    
    def on_message(self, message_type: str):
        """Decorator for message handlers"""
        def decorator(func: Callable):
            self.handlers[message_type] = func
            return func
        return decorator
    
    async def handle_message(self, connection: WebSocketConnection, message: Dict[str, Any]):
        """Handle incoming message"""
        message_type = message.get('type')
        
        if message_type in self.handlers:
            handler = self.handlers[message_type]
            
            if asyncio.iscoroutinefunction(handler):
                await handler(connection, message)
            else:
                handler(connection, message)
