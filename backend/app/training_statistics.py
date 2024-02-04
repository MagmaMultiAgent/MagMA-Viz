import gzip
import pickle

import numpy as np

from backend.utils.types import PropertyData, StepData, EpisodeData, TrainingDataBatch


class Episode:

	@staticmethod
	def property_to_native(property_data: PropertyData) -> PropertyData:
		return {
			"data": property_data["data"].tolist() if isinstance(property_data["data"], np.ndarray) else property_data["data"],
			"tags": property_data["tags"],
			"dimensions": list(property_data["dimensions"])
		}

	def __init__(self, ind: int, episode_data: EpisodeData = None):
		if episode_data is None:
			episode_data = {}

		self.ind = ind
		self.episode_data: EpisodeData = episode_data

	def get(self, step: int) -> StepData | None:
		return self.episode_data.get(step, None)

	def get_property(self, step: int, property_name: str) -> PropertyData | None:
		step_data = self.get(step)
		if step_data is None:
			return None

		data = step_data.get(property_name, None)

		if data is None:
			return None

		return self.property_to_native(data)

	def __getitem__(self, step: int) -> StepData | None:
		return self.get(step)

	def get_multiple(self, steps: list[int]) -> dict[int, StepData]:
		return {step: self.get(step) for step in steps if step in self.episode_data}

	def __getslice__(self, start: int, end: int) -> dict[int, StepData]:
		return self.get_multiple(list(range(start, end)))

	def add(self, episode_data: EpisodeData):
		self.episode_data = self.episode_data | episode_data

	def get_steps(self) -> list[int]:
		return sorted(list(self.episode_data.keys()))

	def get_properties(self) -> dict[int, list[str]]:
		return {step: list(step_data.keys()) for step, step_data in self.episode_data.items()}

	def get_max_step(self) -> int:
		return max(self.get_steps(), default=0)

	def get_missing_steps(self) -> list[int]:
		return [step for step in range(self.get_max_step() + 1) if step not in self.get_steps()]

	def to_dict(self) -> EpisodeData:
		return {step: {property_name: self.property_to_native(data) for property_name, data in step_data.items()} for step, step_data in self.episode_data.items()}

class TrainingStatistics:

	@staticmethod
	def decompress_data_to_send(received: bytes) -> TrainingDataBatch:
		return pickle.loads(gzip.decompress(received))

	def __init__(self):
		self.training_statistics: dict[int, Episode] = {}

	def get_episodes(self) -> list[int]:
		return sorted(list(self.training_statistics.keys()))

	def get_max_episode(self) -> int:
		return max(self.get_episodes())

	def get_missing_episodes(self) -> list[int]:
		return [episode for episode in range(self.get_max_episode() + 1) if episode not in self.get_episodes()]

	def get_steps(self) -> dict[int, list[int]]:
		return {episode: self.training_statistics[episode].get_steps() for episode in self.get_episodes()}

	def get_properties(self) -> dict[int, dict[int, list[str]]]:
		return {episode: self.training_statistics[episode].get_properties() for episode in self.get_episodes()}

	def get_max_step(self) -> int:
		return max([episode.get_max_step() for episode in self.training_statistics.values()])

	def get_missing_steps(self) -> dict[int, list[int]]:
		return {episode: self.training_statistics[episode].get_missing_steps() for episode in self.get_episodes()}

	def get_property(self, episode: int, step: int, property_name: str) -> PropertyData | None:
		return self.training_statistics[episode].get_property(step, property_name)

	def add(self, received: bytes):
		batch = self.decompress_data_to_send(received)
		assert isinstance(batch, list), f"Batch must be a list instead of {type(batch)}"

		episodes: dict = {}
		for element in batch:
			assert isinstance(element, dict), f"Batch element must be a dictionary: {element}"

			episode = element.get("episode", 0)
			step = element["step"]
			property_name = element["property_name"]
			tags = element.get("tags", ["default"])
			data = element["data"]

			assert isinstance(data, float) or isinstance(data, np.ndarray), f"Data must be a floating point number or np.ndarray: {data}"

			if isinstance(data, np.ndarray):
				assert len(data.shape) == 2 or len(data.shape) == 3, f"Numpy array must be grayscale matrix with 2 dimensions or RGB matrix with 3 dimensions. Received: {len(data.shape)}"
				if len(data.shape) == 2:
					assert data.dtype == float, f"Grayscale Numpy array must be of type np.float64. Received: {data.dtype}"
				else:
					assert data.dtype == int, f"RGB Numpy array must be of type np.int64. Received: {data.dtype}"

				visualization_dimensions = data.shape
			else:
				assert isinstance(data, float), f"Data must be a floating point number. Received: {type(data)}"
				visualization_dimensions = (1,)

			if episode not in episodes:
				episodes[episode] = {}
			if step not in episodes[episode]:
				episodes[episode][step] = {}
			if property_name not in episodes[episode][step]:
				episodes[episode][step][property_name] = {}

			episodes[episode][step][property_name] = {
				"data": data,
				"tags": tags,
				"dimensions": visualization_dimensions
			}

		for episode_id, episode_data in episodes.items():
			if episode_id not in self.training_statistics:
				self.training_statistics[episode_id] = Episode(episode_id, episode_data)
			else:
				self.training_statistics[episode_id].add(episode_data)

	def to_dict(self) -> dict[int, EpisodeData]:
		return {episode: self.training_statistics[episode].to_dict() for episode in self.get_episodes()}
