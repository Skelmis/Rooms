import asyncio
import datetime
import json

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect, WebSocket

from rooms import ConnectionManager, Message, Connection, DataT

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
manager = ConnectionManager()


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/{conn_id}/{name}")
async def websocket_endpoint(websocket: WebSocket, conn_id: int, name: str):
    try:
        connection: Connection = Connection(
            conn_id=conn_id, name=name, websocket=websocket, current_conversation_id=1
        )
        manager.register(connection)

        await websocket.accept()

        try:
            while True:
                data: str = await websocket.receive_text()
                data: DataT = json.loads(data)
                sender = manager.get_author(data["sender_conn_id"])
                name = sender.name
                _id = sender.conn_id
                if data["type"] == 1:
                    # MESSAGE SEND
                    message = Message(
                        conversation_id=sender.current_conversation_id,
                        content=data["content"],
                        sender_conn_id=sender.conn_id,
                        sender_name=name,
                        sent_at=datetime.datetime.utcnow().isoformat(),
                    )
                    await manager.send_message_in_conversation(message)
                    print(
                        f"INFO:     {name}({_id}) in conversation {message.conversation_id} said '{message.content}'"
                    )

                elif data["type"] == 2:
                    # CONVERSATION SWITCH
                    new_id = data["conversation_id"]
                    await manager.connect_to_conversation(
                        data["sender_conn_id"], new_id
                    )
                    print(f"INFO:     {name}({_id}) switched to conversation {new_id}")

        except WebSocketDisconnect as e:
            # manager.disconnect(cluster_id)
            raise e
    except Exception as e:
        # manager.disconnect(cluster_id)
        raise e
