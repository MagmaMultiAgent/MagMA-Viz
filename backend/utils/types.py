from typing import TypedDict
from typing_extensions import Required, NotRequired
from enum import Enum

import numpy as np


EnvId = int
EpisodeId = int
StepId = int
PropertyName = str
PossibleDTypes = int | float | str
PossibleDataTypes = PossibleDTypes | np.ndarray

class InferredDataType(Enum):
	OTHER = 0
	SCALAR = 1
	VECTOR = 2
	GENERAL_MATRIX = 3
	RGB_MATRIX = 4
	GRAYSCALE_MATRIX = 5


class TrainingData(TypedDict):
	property_name: Required[PropertyName]
	env: NotRequired[EnvId]
	episode: NotRequired[EpisodeId]
	step: Required[StepId]
	tags: NotRequired[list[str]]
	data: Required[float | np.ndarray]
	file_name: NotRequired[str]

TrainingDataBatch = list[TrainingData]


class EnvData(TypedDict):
	data: Required[PossibleDTypes | np.ndarray]
	tags: Required[list[str]]
	dimension: Required[tuple[int]]
	inferred_data_type: Required[InferredDataType]
	dtype: Required[str]
	file_name: Required[str]

class EnvDataNative(TypedDict):
	data: Required[PossibleDTypes | list[PossibleDTypes] | list[list[PossibleDTypes]] | list[list[list[PossibleDTypes]]]]
	tags: Required[list[str]]
	dimension: Required[list[int]]
	inferred_data_type: Required[str]
	dtype: Required[str]
	file_name: Required[str]

StepData = dict[EnvId, EnvData]
EpisodeData = dict[StepId, StepData]
PropertyData = dict[EpisodeId, EpisodeData]

StepDataNative = dict[EnvId, EnvDataNative]
EpisodeDataNative = dict[StepId, StepDataNative]
PropertyDataNative = dict[EpisodeId, EpisodeDataNative]

class PropertyInfo(TypedDict):
	dimension: Required[tuple[int]]
	inferred_data_type: Required[InferredDataType]
	dtype: Required[str]
	step_ids: Required[dict[EpisodeId, dict[StepId, list[EnvId]]]]

class PropertyInfoNative(TypedDict):
	dimension: Required[list[int]]
	inferred_data_type: Required[str]
	dtype: Required[str]
	step_ids: Required[dict[EpisodeId, dict[StepId, list[EnvId]]]]
