let ws, id, name;
function sendMessage(event) {
    let input = document.getElementById("messageText")
    ws.send(`{"content": "${input.value}", "sender_conn_id": ${id}, "type": 1}`)
    input.value = ''
    event.preventDefault()
}

function createWS(event) {
    name = document.getElementById('ws_username')
    id = Math.floor(Math.random() * 90000)
    ws = new WebSocket(`ws://localhost:4567/ws/${id}/${name.value}`)
    name.value = ''
    ws.onmessage = function (event) {
        let messages = document.getElementById('messages')
        let message = document.createElement('li')
        let content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
    };
    event.preventDefault()
    // TODO Hide join form
}

function changeTo(event) {
    let val = document.getElementById('conversation_id');
    ws.send(`{"content": "", "sender_conn_id": ${id}, "conversation_id": ${val.value}, "type": 2}`)
    event.preventDefault()
    val.value = ''

    // Clear the old messages
    let messages = document.getElementById('messages')
    messages.innerHTML = ''
}