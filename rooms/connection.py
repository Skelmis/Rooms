from dataclasses import dataclass

from starlette.websockets import WebSocket


@dataclass
class Connection:
    conn_id: int
    name: str
    websocket: WebSocket
    current_conversation_id: int | None = None
