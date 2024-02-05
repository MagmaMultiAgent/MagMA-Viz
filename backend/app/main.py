import os
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from backend.utils.logging_config import configure_logging
configure_logging()

from backend.app.connection_manager import ConnectionManager
from backend.app.udp_endpoint import UDPEndpoint
from backend.app.training_statistics import TrainingStatistics


UDP_HOST = os.environ.get("VISUALIZATION_HOST", "0.0.0.0")
UDP_PORT = os.environ.get("VISUALIZATION_PORT", 8001)


# App

app = FastAPI()


# Middleware

origins = ["*"]
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


# Routes

here = Path(__file__).parent
frontend_path = here.parent.parent / "frontend" / "MagmaViz"

static_path = frontend_path / "static"
build_path = frontend_path / "build"

# client can send get requests to get data from train statistics
@app.get("/api/get_data")
async def get_data(episode: int, step: int, propertyName: str):
	data = train_statistics.get_property(episode, step, propertyName)
	if data is None:
		return JSONResponse(content="", status_code=404)
	return JSONResponse(data)

# initialize websocket connection
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
	await manager.connect(websocket)
	try:
		while True:
			data = await websocket.receive_text()
			print(f"{client_id} sent {data}")
	except WebSocketDisconnect:
		manager.disconnect(websocket)

app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/", StaticFiles(directory=build_path, html=True), name="frontend")

# catchall route for frontend
@app.get("/{path:path}")
def read_path(path: str):
	return FileResponse(build_path / "index.html")


# Events

@app.on_event("startup")
async def on_startup() -> None:
	loop = asyncio.get_running_loop()
	transport, protocol = await loop.create_datagram_endpoint(
		lambda: UDPEndpoint(loop, train_statistics, manager), local_addr=(UDP_HOST, UDP_PORT)
	)
	app.state.udp_transport = transport
	app.state.udp_protocol = protocol

@app.on_event("shutdown")
async def on_shutdown() -> None:
	app.state.udp_transport.close()


# Connections

train_statistics = TrainingStatistics()
manager = ConnectionManager(train_statistics)

