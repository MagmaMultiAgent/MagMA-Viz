import socket
import time
import numpy as np
import io
import gzip
from pickle import dumps, loads


ADDRESS = "127.0.0.1"
UDP_PORT = 8001

addr = socket.getaddrinfo(
	ADDRESS, UDP_PORT,
	socket.AF_INET, socket.SOCK_DGRAM)[0]

def make_data_to_send():
	width = 64
	height = 64

	base_color = [255, 255, 255]
	obstacle_color = [192, 192, 192]
	unit_color = [0, 102, 204]

	board = np.zeros((height, width, 3))
	board[board[:, :, 0] == 0] = base_color

	obstacle_chance = 0.5
	obstacle_coords = np.where(np.random.rand(height, width) < obstacle_chance)
	board[obstacle_coords] = obstacle_color

	unit_chance = 0.1
	unit_coords = np.where(np.random.rand(height, width) < unit_chance)
	board[unit_coords] = unit_color

	return board


with socket.socket(*addr[:3]) as s:
	s.connect(addr[4])

	for i in range(100):
			
		board = make_data_to_send()
		compressed = gzip.compress(board.tobytes())
		
		s.send(compressed)
