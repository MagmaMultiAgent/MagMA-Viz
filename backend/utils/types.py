from typing import TypedDict
from typing_extensions import Required, NotRequired
import numpy as np

EpisodeId = int
StepId = int
PropertyName = str

class PropertyData(TypedDict):
	data: Required[float | np.ndarray]
	tags: Required[list[str]]
	dimensions: Required[list[int]]

class PropertyDataNative(TypedDict):
	data: Required[float | list[list[float]] | list[list[list[int]]]]
	tags: Required[list[str]]
	dimensions: Required[list[int]]

StepData = dict[PropertyName, PropertyData]
EpisodeData = dict[StepId, StepData]

class TrainingData(TypedDict):
	episode: NotRequired[EpisodeId]
	step: Required[StepId]
	property_name: Required[PropertyName]
	tags: NotRequired[list[str]]
	data: Required[float | np.ndarray]

TrainingDataBatch = list[TrainingData]
