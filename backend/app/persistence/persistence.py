from typing import Any
from pathlib import Path
import pickle
import gzip

class FilePersistence:
    __HERE = Path(__file__).resolve()
    __PARENT = __HERE.parent
    __SAVE_FOLDER_NAME = "saves"
    SAVE_FOLDER = __PARENT / __SAVE_FOLDER_NAME

    def __init__(self):
        pass

    @staticmethod
    def compress_data(data):
        return gzip.compress(pickle.dumps(data))

    @staticmethod
    def decompress_data(data):
        return pickle.loads(gzip.decompress(data))

    @classmethod
    def save(cls, data: Any, filename: str):
        path = cls.SAVE_FOLDER / filename
        data_compressed = FilePersistence.compress_data(data)
        with open(path, 'wb') as file:
            file.write(data_compressed)

    @classmethod
    def load(cls, filename: str):
        path = cls.SAVE_FOLDER / filename
        with open(path, 'rb') as file:
            data_compressed = file.read()
        return FilePersistence.decompress_data(data_compressed)
