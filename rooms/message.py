from dataclasses import dataclass


@dataclass
class Message:
    content: str
    sent_at: str
    sender_name: str
    sender_conn_id: int
    conversation_id: int
