import numpy as np
import random

import logging
import backend.utils.logging_config

from .client import Client


def make_2d_example():
	width = 64
	height = 64

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


def make_example(episodes: list = None, steps: int = 3):
	if episodes is None:
		episodes = [0]
	data = []
	for episode in episodes:
		for step in range(steps):
			_data = [
				{
					"episode": episode,
					"step": step,
					"property_name": "board",
					"tags": ["tag1"],
					"data": make_2d_example()
				},
				{
					"episode": episode,
					"step": step,
					"property_name": "board",
					"tags": ["tag2"],
					"data": make_2d_example()
				},
				{
					"episode": episode,
					"step": step,
					"property_name": "reward",
					"tags": ["tag1"],
					"data": make_1d_example()
				},
				{
					"episode": episode,
					"step": step,
					"property_name": "reward",
					"tags": ["tag2"],
					"data": make_1d_example()
				},
			]

			data += _data

	return data


client = Client()
client.logger.setLevel(logging.DEBUG)

for _ in range(10):
		
	example = make_example(episodes=[0, 1], steps=3)

	client.send(example)
