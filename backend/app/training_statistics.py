import gzip
import pickle

import numpy as np

import re

from backend.utils.types import EnvData, EnvDataNative, PropertyData, PropertyInfoNative, TrainingDataBatch, PossibleDTypes, PossibleDataTypes, InferredDataType


class Property:
	def __init__(self, name: str, dimension: tuple[int], inferred_data_type: InferredDataType, dtype: str):
		self.name = name
		self.dimension = dimension
		self.inferred_data_type = inferred_data_type
		self.dtype = dtype
		self.data: PropertyData = {}

	@staticmethod
	def data_to_native(data_element: EnvData) -> EnvDataNative:
		return {
			"data": data_element["data"].tolist() if isinstance(data_element["data"], np.ndarray) else data_element["data"],
			"tags": data_element["tags"],
			"dimension": list(data_element["dimension"]),
			"inferred_data_type": data_element["inferred_data_type"].name,
			"dtype": data_element["dtype"]
		}

	def add(self, env: int, episode: int, step: int, tags: list[str], data: PossibleDataTypes, dimension: tuple[int], inferred_data_type: InferredDataType, dtype: str):
		assert dimension == self.dimension, f"Dimension {dimension} does not match the expected dimension {self.dimension}"
		assert inferred_data_type == self.inferred_data_type, f"Inferred visualization type {inferred_data_type} does not match the expected type {self.inferred_data_type}"
		assert dtype == self.dtype, f"Data type {dtype} does not match the expected type {self.dtype}"

		if episode not in self.data:
			self.data[episode] = {}
		if step not in self.data[episode]:
			self.data[episode][step] = {}
		self.data[episode][step][env] = {
			"data": data,
			"tags": tags,
			"dimension": dimension,
			"inferred_data_type": inferred_data_type,
			"dtype": dtype
		}

	def get_step_ids(self) -> dict[int, dict[int, list[int]]]:
		step_ids = {}
		for episode, steps in self.data.items():
			step_ids[episode] = {}
			for step, envs in steps.items():
				step_ids[episode][step] = list(envs.keys())
		return step_ids

class TrainingStatistics:
	def __init__(self):
		self.properties = {}

	@staticmethod
	def decompress_data_to_send(received: bytes) -> TrainingDataBatch:
		return pickle.loads(gzip.decompress(received))

	@staticmethod
	def infer_visualization_type(data: PossibleDataTypes) -> tuple[tuple[int], InferredDataType, str]:
		if isinstance(data, np.ndarray):
			dimension = data.shape
			# remove numbers from dtype (e.g. int64) with regex
			dtype = str(data.dtype)
			dtype = re.sub(r"\d", "", dtype)
			if len(dimension) == 1:
				inferred_data_type = InferredDataType.VECTOR
			elif len(dimension) == 2:
				# check if grayscale (every element is a max 255 and int type)
				if np.max(data) <= 255 and np.min(data) >= 0 and data.dtype in (int, float):
					inferred_data_type = InferredDataType.GRAYSCALE_MATRIX
				else:
					inferred_data_type = InferredDataType.GENERAL_MATRIX
			elif len(dimension) == 3:
				if dimension[2] == 3 and np.max(data) <= 255 and np.min(data) >= 0 and data.dtype in (int, float):
					inferred_data_type = InferredDataType.RGB_MATRIX
				elif np.max(data) <= 255 and np.min(data) >= 0 and data.dtype in (int, float):
					inferred_data_type = InferredDataType.GRAYSCALE_MATRIX
				else:
					inferred_data_type = InferredDataType.GENERAL_MATRIX
			else:
				inferred_data_type = InferredDataType.OTHER
		else:
			assert isinstance(data, PossibleDTypes), f"Scalar value must be integer, float or string instead of {type(data)}"
			dimension = (1,)
			inferred_data_type = InferredDataType.SCALAR
			dtype = type(data).__name__

		return dimension, inferred_data_type, dtype

	def add(self, received: bytes):
		batch = self.decompress_data_to_send(received)
		assert isinstance(batch, list), f"Batch must be a list of dictionaries instead of {type(batch)}"

		for element in batch:
			assert isinstance(element, dict), f"Batch element must be a dictionary: {element}"

			property_name = element["property_name"]
			env = element.get("env", 0)
			episode = element.get("episode", 0)
			step = element["step"]
			tags = element.get("tags", ["default"])
			data = element["data"]

			assert isinstance(property_name, str), f"Property name must be a string instead of {type(property_name)}"
			assert isinstance(env, int), f"Environment ID must be an integer instead of {type(env)}"
			assert isinstance(episode, int), f"Episode ID must be an integer instead of {type(episode)}"
			assert isinstance(step, int), f"Step ID must be an integer instead of {type(step)}"
			assert isinstance(tags, list), f"Tags must be a list of strings instead of {type(tags)}"
			for tag in tags:
				assert isinstance(tag, str), f"A tag must be a string instead of {type(tag)}"

			assert isinstance(data, PossibleDataTypes), f"Data must be a scalar value or a Numpy array instead of {type(data)}"

			dimension, inferred_data_type, dtype = self.infer_visualization_type(data)

			if property_name not in self.properties:
				self.properties[property_name] = Property(property_name, dimension, inferred_data_type, dtype)
			self.properties[property_name].add(env, episode, step, tags, data, dimension, inferred_data_type, dtype)

	def get_properties(self) -> list[str]:
		return sorted(list(self.properties.keys()))

	def get_property(self, property_name: str) -> Property | None:
		if property_name not in self.properties:
			return None
		return self.properties[property_name]

	def get_property_info(self, property_name: str) -> PropertyInfoNative | None:
		if property_name not in self.properties:
			return None

		prop = self.properties[property_name]
		return {
			"dimension": prop.dimension,
			"inferred_data_type": prop.inferred_data_type.name,
			"dtype": prop.dtype,
			"step_ids": prop.get_step_ids()
		}

	def get_property_infos(self) -> dict[str, PropertyInfoNative]:
		return {prop: self.get_property_info(prop) for prop in self.get_properties()}

	def get_data_for_property(self, property_name: str) -> dict[int, dict[int, dict[int, EnvDataNative]]] | None:
		if property_name not in self.properties:
			return None
		prop = self.properties[property_name]
		data = {}
		for episode, steps in prop.data.items():
			data[episode] = {}
			for step, envs in steps.items():
				data[episode][step] = {}
				for env, env_data in envs.items():
					data[episode][step][env] = prop.data_to_native(env_data)
		return data

	def get_data_for_episode(self, property_name: str, episode: int) -> dict[int, dict[int, EnvDataNative]] | None:
		if property_name not in self.properties:
			return None
		prop = self.properties[property_name]
		data = {}
		if episode not in prop.data:
			return None
		for step, envs in prop.data[episode].items():
			data[step] = {}
			for env, env_data in envs.items():
				data[step][env] = prop.data_to_native(env_data)
		return data

	def get_data_for_step(self, property_name: str, episode: int, step: int) -> dict[int, EnvDataNative] | None:
		if property_name not in self.properties:
			return None
		prop = self.properties[property_name]
		data = {}
		if episode not in prop.data or step not in prop.data[episode]:
			return None
		for env, env_data in prop.data[episode][step].items():
			data[env] = prop.data_to_native(env_data)
		return data

	def get_data_for_env(self, property_name: str, episode: int, step: int, env: int) -> EnvDataNative | None:
		if property_name not in self.properties:
			return None
		prop = self.properties[property_name]
		if episode not in prop.data or step not in prop.data[episode] or env not in prop.data[episode][step]:
			return None
		return prop.data_to_native(prop.data[episode][step][env])
