import asyncio
import json
import logging
import traceback


class UDPEndpoint(asyncio.DatagramProtocol):
	def __init__(self, loop, train_statistics, manager):
		self.logger = logging.getLogger(self.__class__.__name__)
		self.loop = loop
		super().__init__()
		self.transport = None

		self.train_statistics = train_statistics
		self.manager = manager

	def connection_made(self, transport: asyncio.DatagramTransport) -> None:
		self.transport = transport
		self.logger.info(f"UDP endpoint started at {transport.get_extra_info('sockname')}")
		self.logger.info(f"Client connected: {self.manager.active_connections}")

	def datagram_received(self, received: bytes, addr: tuple[str, int]) -> None:
		self.logger.info(f"Received data from {addr} with {len(received)} bytes.")
		self.logger.info(f"Sending to {len(self.manager.active_connections)} clients.")

		try:
			self.train_statistics.add(received)
		except Exception:
			self.logger.error(f"Error while parsing train statistics")
			self.logger.error(traceback.format_exc())
			return

		properties = json.dumps(self.train_statistics.get_property_infos())
		self.loop.create_task(self.manager.broadcast(properties))
