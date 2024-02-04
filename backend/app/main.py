import os
import traceback
import json
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
import asyncio

import logging
import backend.utils.logging_config

from backend.app.training_statistics import TrainingStatistics


UDP_HOST = os.environ.get("VISUALIZATION_HOST", "0.0.0.0")
UDP_PORT = os.environ.get("VISUALIZATION_PORT", 8001)

app = FastAPI()


# Websocket

# here path
here = Path(__file__).parent
basic_html_path = here.parent.parent / "frontend" / "basic_page.html"

with open(str(basic_html_path), "r") as file:
	html = file.read()

@app.get("/")
async def root():
	return HTMLResponse(html)

@app.get("/")
async def get():
	return HTMLResponse(html)


# client can send get requests to get data from train statistics
@app.get("/get_data")
async def get_data(episode: int, step: int, property: str):
	data = train_statistics.get_property(episode, step, property)
	if data is None:
		return JSONResponse(content="", status_code=404)
	return JSONResponse(data)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
	await manager.connect(websocket)
	try:
		while True:
			data = await websocket.receive_text()
			print(f"{client_id} sent {data}")
	except WebSocketDisconnect:
		manager.disconnect(websocket)


# Connections

class ConnectionManager:
	def __init__(self):
		self.active_connections: list[WebSocket] = []

	async def connect(self, websocket: WebSocket):
		await websocket.accept()
		self.active_connections.append(websocket)
		steps = json.dumps(train_statistics.get_properties())
		await websocket.send_text(steps)

	def disconnect(self, websocket: WebSocket):
		self.active_connections.remove(websocket)

	@staticmethod
	async def send_personal_message(message: str, websocket: WebSocket):
		await websocket.send_text(message)

	async def broadcast(self, message: str):
		for connection in self.active_connections:
			await connection.send_text(message)

manager = ConnectionManager()

train_statistics = TrainingStatistics()

# UDP

class UDPEndpoint(asyncio.DatagramProtocol):
	def __init__(self, loop):
		self.logger = logging.getLogger(self.__class__.__name__)
		self.loop = loop
		super().__init__()
		self.transport = None

	def connection_made(self, transport: asyncio.DatagramTransport) -> None:
		self.transport = transport
		self.logger.info(f"UDP endpoint started at {transport.get_extra_info('sockname')}")
		self.logger.info(f"Client connected: {manager.active_connections}")

	def datagram_received(self, received: bytes, addr: tuple[str, int]) -> None:
		self.logger.info(f"Received data from {addr} with {len(received)} bytes.")
		self.logger.info(f"Sending to {len(manager.active_connections)} clients.")

		try:
			train_statistics.add(received)
		except Exception:
			self.logger.error(f"Error while parsing train statistics")
			self.logger.error(traceback.format_exc())
			return

		steps = json.dumps(train_statistics.get_properties())
		self.loop.create_task(manager.broadcast(steps))

@app.on_event("startup")
async def on_startup() -> None:
	loop = asyncio.get_running_loop()
	transport, protocol = await loop.create_datagram_endpoint(
		lambda: UDPEndpoint(loop), local_addr=(UDP_HOST, UDP_PORT)
	)
	app.state.udp_transport = transport
	app.state.udp_protocol = protocol

@app.on_event("shutdown")
async def on_shutdown() -> None:
	app.state.udp_transport.close()
