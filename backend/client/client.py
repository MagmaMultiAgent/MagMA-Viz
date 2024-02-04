import socket
import atexit
import os

import pickle
import gzip

import logging
import backend.utils.logging_config

from backend.utils.types import TrainingDataBatch


def exit_handler(socket_to_close):
	# This function will be called on program exit
	if socket_to_close:
		socket_to_close.close()

class Client:
	VISUALIZATION_HOST = os.environ.get("VISUALIZATION_HOST", "localhost")
	VISUALIZATION_PORT = os.environ.get("VISUALIZATION_PORT", 8001)
	VISUALIZATION_ADDRESS = socket.getaddrinfo(
								VISUALIZATION_HOST, VISUALIZATION_PORT,
								socket.AF_INET, socket.SOCK_DGRAM)[0]
	READABLE_VISUALIZATION_ADDRESS = (VISUALIZATION_ADDRESS[4][0], VISUALIZATION_ADDRESS[4][1])

	@staticmethod
	def compress_data_to_send(batch: TrainingDataBatch) -> bytes:
		return gzip.compress(pickle.dumps(batch))

	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)

		self.socket = socket.socket(*self.__class__.VISUALIZATION_ADDRESS[:3])
		self.socket.setblocking(False)
		atexit.register(exit_handler, self.socket)
		self.socket.connect(self.__class__.VISUALIZATION_ADDRESS[4])

	def send(self, batch: TrainingDataBatch):
		# TODO: if the packet is too large, split it into smaller packets

		compressed_batch = self.compress_data_to_send(batch)
		self.logger.debug(f"Sending batch of {len(batch)} with size {len(compressed_batch)} to {self.__class__.READABLE_VISUALIZATION_ADDRESS}")
		self.socket.send(compressed_batch)
