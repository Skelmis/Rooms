from typing import TypedDict, Literal


class DataT(TypedDict):
    sender_conn_id: int
    type: Literal[1, 2]
    content: str | None
    conversation_id: int | None


class MessageT(TypedDict):
    sender_conn_id: int
    type: Literal[1]
    content: str


class ChangeT(TypedDict):
    sender_conn_id: int
    type: Literal[2]
    conversation_id: int
