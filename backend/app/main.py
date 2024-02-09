import os
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio

import logging
from backend.utils.logging_config import configure_logging
configure_logging()

from backend.app.connection_manager import ConnectionManager
from backend.app.udp_endpoint import UDPEndpoint
from backend.app.training_statistics import TrainingStatistics


UDP_HOST = os.environ.get("VISUALIZATION_HOST", "0.0.0.0")
UDP_PORT = os.environ.get("VISUALIZATION_PORT", 8001)


# App

app = FastAPI()

logger = logging.getLogger(__name__)


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
@app.get("/api/getPropertyInfo")
async def get_property_info(propertyName: str):
	global logger
	property_info = train_statistics.get_property_info(propertyName)
	if property_info is None:
		logger.error(f"Property {propertyName} not found")
		property_info = {}
	return JSONResponse(property_info)

@app.get("/api/getAllData")
async def get_all_data(propertyName: str):
	global logger
	data = train_statistics.get_data_for_property(propertyName)
	if data is None:
		logger.error(f"Property {propertyName} not found")
		data = {}
	return JSONResponse(data)

@app.get("/api/getDataForEpisode")
async def get_data_for_episode(propertyName: str, episode: int):
	global logger
	data = train_statistics.get_data_for_episode(propertyName, episode)
	if data is None:
		logger.error(f"Property {propertyName} not found")
		data = {}
	return JSONResponse(data)

@app.get("/api/getDataForStep")
async def get_data_for_step(propertyName: str, episode: int, step: int):
	global logger
	data = train_statistics.get_data_for_step(propertyName, episode, step)
	if data is None:
		logger.error(f"Property {propertyName} not found")
		data = {}
	return JSONResponse(data)

@app.get("/api/getDataForEnv")
async def get_data_for_env(propertyName: str, episode: int, step: int,  env: int):
	global logger
	data = train_statistics.get_data_for_env(propertyName, episode, step, env)
	if data is None:
		logger.error(f"Property {propertyName} not found")
		data = {}
	return JSONResponse(data)



# initialize websocket connection
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
	await manager.connect(websocket)
	try:
		while True:
			data = await websocket.receive_text()
	except WebSocketDisconnect:
		manager.disconnect(websocket)

app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/", StaticFiles(directory=build_path, html=True), name="frontend")

# catchall route for frontend
@app.get("/{path:path}")
def read_path(path: str):
	_ = path
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

