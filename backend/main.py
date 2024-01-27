from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
import numpy as np
import io
import gzip
import json

from typing import Dict, Tuple


ADDRESS = "0.0.0.0"
UDP_PORT = 8001


app = FastAPI()


# Websocket

html = """
<!DOCTYPE html>
<html>
	<head>
		<title>TrainStreamer</title>
		<style>
			#container {
			   border-collapse: collapse;
			}

			/* And this to your table's `td` elements. */
			#container td {
			   padding: 0;
			   margin: 0;
			   width: 10px;
			   height: 10px;
			}

			#slidecontainer {
				display: flex;
				flex-direction: row;
			}
		</style>
	</head>
	<body>
		<h1>Lux AI 2</h1>
		<div>Hello there!</div>
		<div id="slidecontainer">
			<button id="decreaseState" type="button">-</button>
			<input type="range" min="1" max="1" value="1" class="slider" id="stateSlider">
			<button id="increaseState" type="button">+</button>
		</div>
		<span>State:</span>
		<span id="currentState" style="font-weight:bold;color:red">1</span>
		<div id="messages"></div>
		<table id="container">

		</table>
		<script>
			var container = document.querySelector("table#container");
			var slider = document.querySelector("input#stateSlider");
			var decreaseStateButton = document.querySelector("button#decreaseState");
			var increaseStateButton = document.querySelector("button#increaseState");
			var currentStateElement = document.querySelector("span#currentState");
			var states = [];
			var current_state = 1;

			slider.oninput = function() {
				current_state = this.value;

				console.log("Slider set to", current_state);
				currentStateElement.innerHTML = current_state + " / " + states.length;
				draw_table(current_state - 1);
			}

			decreaseStateButton.onclick = function() {
				if(current_state <= 1) {
					return;
				}
				current_state -= 1;
				slider.setAttribute("value", current_state);
				console.log("Slider set to", current_state);
				currentStateElement.innerHTML = current_state + " / " + states.length;
				draw_table(current_state - 1);
			}

			increaseStateButton.onclick = function() {
				if(current_state >= states.length) {
					return;
				}
				current_state += 1;
				slider.setAttribute("value", current_state);
				console.log("Slider set to", current_state);
				currentStateElement.innerHTML = current_state + " / " + states.length;
				draw_table(current_state - 1);
			}

			function adjust_slider(){
				slider.setAttribute("max", states.length);
				currentStateElement.innerHTML = current_state + " / " + states.length;
			}

			function draw_table(state){
				if(state >= states.length) {
					console.log("Can't draw index", state);
					return;
				}

				console.log("Drawing index", state);

				var arrays = states[state];
				container.innerHTML = '';
				for (var i = 0; i < arrays.length; i++) {
					var row = container.insertRow(i);

					for (var j = 0; j < arrays[i].length; j++) {
						var cell = row.insertCell(j);

						var red = arrays[i][j][0];
						var green = arrays[i][j][1];
						var blue = arrays[i][j][2];

						cell.style.backgroundColor = "rgb(" + red + ", " + green + ", " + blue + ")";
						cell.style.border = "1px solid lightgray";
					}
				}
			}

			var client_id = Date.now();
			var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
			ws.onmessage = function(event) {
				var arrays_str = event.data;
				var arrays = JSON.parse(arrays_str);
				states.push(arrays);
				adjust_slider();

				if(states.length == 1) {
					draw_table(0);
				}
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
		print(f"Received data from {addr}")
		print(f"Sending to {len(manager.active_connections)} clients.")

		decompressed_data = gzip.decompress(data)
		arr = np.frombuffer(decompressed_data, dtype=np.float64).reshape(64, 64, 3)
		arr_list = arr.tolist()
		arr_json = json.dumps(arr_list)

		print(f"Received {len(data)} bytes via UDP")
		self.loop.create_task(manager.broadcast(arr_json))


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
