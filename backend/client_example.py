import numpy as np
import random
import sys
import traceback

import logging

try:
	from MagmaVizClient.client import Client
except ImportError:
	print(traceback.format_exc())
	print("MagmaVizClient is not installed. Please install the package from the /backend/client/MagmaVizClient folder.", file=sys.stderr)
	sys.exit(1)


def make_2d_grayscale_example(size: int = 64):
	width = size
	height = size

	base_color = 255
	obstacle_color = 192
	unit_color = 0

	board = np.zeros((height, width), dtype=np.int64)
	board[board == 0] = base_color

	obstacle_chance = 0.5
	obstacle_coords = np.where(np.random.rand(height, width) < obstacle_chance)
	board[obstacle_coords] = obstacle_color

	unit_chance = 0.1
	unit_coords = np.where(np.random.rand(height, width) < unit_chance)
	board[unit_coords] = unit_color

	return board

def make_2d_rgb_example(size: int = 64):
	width = size
	height = size

	base_color = [255, 255, 255]
	obstacle_color = [192, 192, 192]
	unit_color = [0, 102, 204]

	board = np.zeros((height, width, 3), dtype=np.int64)
	board[board[:, :, 0] == 0] = base_color

	obstacle_chance = 0.5
	obstacle_coords = np.where(np.random.rand(height, width) < obstacle_chance)
	board[obstacle_coords] = obstacle_color

	unit_chance = 0.1
	unit_coords = np.where(np.random.rand(height, width) < unit_chance)
	board[unit_coords] = unit_color

	return board

def make_1d_example():
	return random.random()


def make_example(step_start_ind: int = 0, steps: int = 10):
	envs = [0, 1, 3, 4]
	data = []

	for _step in range(steps):
		step = _step + step_start_ind
		episode = step // 10
		for env in envs:
			_data = [
				{
					"env": env,
					"episode": episode,
					"step": step,
					"property_name": "board1",
					"tags": ["tag1"],
					"data": make_2d_rgb_example()
				},
				{
					"env": env,
					"episode": episode,
					"step": step,
					"property_name": "board2",
					"tags": ["tag2"],
					"data": make_2d_rgb_example()
				},
				{
					"env": env,
					"episode": episode,
					"step": step,
					"property_name": "board3",
					"tags": ["tag3"],
					"data": make_2d_grayscale_example()
				},
				{
					"env": env,
					"episode": episode,
					"step": step,
					"property_name": "reward1",
					"tags": ["tag4"],
					"data": make_1d_example()
				},
				{
					"env": env,
					"episode": episode,
					"step": step,
					"property_name": "reward2",
					"tags": ["tag5"],
					"data": make_1d_example()
				},
			]

			data += _data

	return data


client = Client()
client.logger.setLevel(logging.DEBUG)

messages = 100
for i in range(messages):

	if i % 10 == 0:
		print(f"{i} / {messages}")
		
	example = make_example(i*1, 1)
	client.send(example)
