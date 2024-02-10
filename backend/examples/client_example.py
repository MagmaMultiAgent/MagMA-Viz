import numpy as np
import random
import sys
import traceback
from concurrent.futures import ProcessPoolExecutor


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


def train_env(env_id: int = 0, steps: int = 100):
	print(f"Training env {env_id} for {steps} steps")

	observation_client = Client()
	reward_client = Client()

	for i in range(steps):

		if ((i+1) % 10) == 0:
			print(f"Env {env_id}: {i+1} / {steps}")

		observation = {
			"observation": None,
			"stream_data": {
				"board1": make_2d_rgb_example(16),
				"board2": make_2d_rgb_example(128),
				"board3": make_2d_grayscale_example(64)
			}
		}
		stream_data = observation["stream_data"]
		episode_id = i // 10
		data_to_send = []
		for property_name, data in stream_data.items():
			data_to_send.append({
				"property_name": property_name,
				"env": env_id,
				"episode": episode_id,
				"step": i,
				"data": data
			})
		observation_client.send(data_to_send)

		reward = make_1d_example()
		reward_client.send([{
			"property_name": "reward",
			"env": env_id,
			"episode": episode_id,
			"step": i,
			"data": reward
		}])

env_count = 4
steps_per_env = 100

processes = []
with ProcessPoolExecutor(max_workers=env_count) as process_pool:
	for i in range(env_count):
		future = process_pool.submit(train_env, i, steps_per_env)
		processes.append(future)

for process in processes:
	process.result()
