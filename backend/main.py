from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio

from typing import Dict, Tuple


ADDRESS = "127.0.0.1"
UDP_PORT = 8001


app = FastAPI()


# Websocket

html = """
<!DOCTYPE html>
<html>
	<head>
		<title>TrainStreamer</title>
	</head>
	<body>
		<h1>WebSocket Test</h1>
		<div>Hello there!</div>
		<div id="messages"></div>
		<script>
			var client_id = Date.now()
			var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
			ws.onmessage = function(event) {
				var promise = event.data.text();

				var messages = document.getElementById('messages')
				var message = document.createElement('li')
				var res = promise.then(r => {
					console.log("Recieved:", r);
					var content = document.createTextNode(r);
					message.appendChild(content)
				});
				messages.appendChild(message)
			};
			function sendMessage(event) {
				ws.send("hi")
				event.preventDefault()
			}
		</script>
	</body>
</html>
"""

@app.get("/")
async def root():
	return HTMLResponse(html)

class ConnectionManager:
	def __init__(self):
		self.active_connections: list[WebSocket] = []

	async def connect(self, websocket: WebSocket):
		await websocket.accept()
		self.active_connections.append(websocket)

	def disconnect(self, websocket: WebSocket):
		self.active_connections.remove(websocket)

	async def send_personal_message(self, message: str, websocket: WebSocket):
		await websocket.send_text(message)

	async def broadcast(self, message: str):
		for connection in self.active_connections:
			await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
	return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
	await manager.connect(websocket)
	try:
		while True:
			data = await websocket.receive_text()
			print(f"{client_id} sent {data}")
	except WebSocketDisconnect:
		manager.disconnect(websocket)


# UDP

class UDPEndpoint(asyncio.DatagramProtocol):
	def __init__(self, loop):
		self.loop = loop
		super().__init__()

	def connection_made(self, transport: asyncio.DatagramTransport) -> None:
		self.transport = transport
		print("UTP endpoint started!")
		print(f"Clients connected: {manager.active_connections}")

	def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
		print(f"Received {data} from {addr}")
		print(f"Sendint to {len(manager.active_connections)} clients.")

		data_str = data.decode("utf-8")
		self.loop.create_task(manager.broadcast(data))


@app.on_event("startup")
async def on_startup() -> None:
	loop = asyncio.get_running_loop()
	transport, protocol = await loop.create_datagram_endpoint(
		lambda: UDPEndpoint(loop), local_addr=(ADDRESS, UDP_PORT)
	)
	app.state.udp_transport = transport
	app.state.udp_protocol = protocol


@app.on_event("shutdown")
async def on_shutdown() -> None:
	app.state.udp_transport.close()
