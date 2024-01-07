from typing import Dict, Set, Any

from fastapi import WebSocket

TopicConnections = Dict[str, Set[WebSocket]]
TopicPayload = Any


class WSManager:
    def __init__(self):
        self.active_connections: TopicConnections = {}

    async def connect(self, topic_id: str, ws: WebSocket):
        self.active_connections.setdefault(topic_id, set()).add(ws)

    async def disconnect(self, topic_id: str, ws: WebSocket):
        if topic_id in self.active_connections:
            self.active_connections[topic_id].discard(ws)

    async def send_message(self, topic_id: str, message: TopicPayload):
        for ws in self.active_connections.get(topic_id, []):
            await ws.send_json(message)
