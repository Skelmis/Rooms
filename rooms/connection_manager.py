import json
import logging
from dataclasses import asdict
from typing import Dict, Union, Optional

from starlette.websockets import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedOK

from rooms import Connection, Message

log = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Connection] = {}
        self.conversation_history: Dict[int, list[Message]] = {}

    def register(self, connection: Connection):
        log.info("Registered a connection for %s", connection.name)
        self.active_connections[connection.conn_id] = connection

    def disconnect(self, conn_id: int):
        log.info("Disconnected a connection for %s", conn_id)
        self.active_connections.pop(conn_id, None)

    def get_author(self, conn_id: int) -> Connection:
        val = self.active_connections.get(conn_id)
        if not val:
            raise RuntimeError(f"Connection doesn't exist with this id, {conn_id}")

        return val

    async def send_message_in_conversation(self, message: Message) -> None:
        if message.conversation_id in self.conversation_history:
            self.conversation_history[message.conversation_id].append(message)
        else:
            self.conversation_history[message.conversation_id] = [message]

        for connection in self.active_connections.values():
            if connection.current_conversation_id == message.conversation_id:
                await connection.websocket.send_json({"data": asdict(message)})

    async def connect_to_conversation(self, conn_id: int, conversation_id: int) -> None:
        connection: Connection | None = self.active_connections.get(conn_id)
        if not connection:
            raise RuntimeError("This connection doesn't exist")

        connection.current_conversation_id = conversation_id

        previous_messages: list[Message] = self.conversation_history.get(
            conversation_id, []
        )
        for message in previous_messages:
            await connection.websocket.send_json({"data": asdict(message)})

    @staticmethod
    def dict_from_str(data: str) -> dict:
        return json.loads(data)
