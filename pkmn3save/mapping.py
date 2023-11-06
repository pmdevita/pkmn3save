import struct
from functools import cached_property


class DataMapping:
    _CACHED_PROPERTIES = []
    _CACHED_PROPERTIES_KNOWN = False

    def __init__(self, data: bytes):
        self._data = data

    @property
    def data(self) -> bytes:
        return self._data

    @data.setter
    def data(self, data: bytes):
        self._data = data

    @classmethod
    def _get_props(cls):
        return [x for x in dir(cls)
                if isinstance(getattr(cls, x), cached_property)]

    def _reset_cache(self):
        if not self.__class__._CACHED_PROPERTIES_KNOWN:
            self.__class__._CACHED_PROPERTIES = self._get_props()

        for attr in self.__class__._CACHED_PROPERTIES:
            delattr(self, attr)


class BinaryChunk:
    def __init__(self, start: int, size: int):
        self.start = start
        self.size = size

    def __call__(self, b: bytes) -> bytes:
        return self.extract(b)

    def extract(self, b: bytes) -> bytes:
        return b[self.start: self.start + self.size]


class StructChunk:
    def __init__(self, format: str, start: int, size: int):
        self.format = format
        self.start = start
        self.size = size

    def __call__(self, b: bytes) -> int:
        return self.extract(b)

    def extract(self, b: bytes) -> int:
        chunk = b[self.start: self.start + self.size]
        num = struct.unpack(self.format, b[self.start: self.start + self.size])[0]
        return num


GAME_SAVE_A = BinaryChunk(0x0, 57344)
GAME_SAVE_B = BinaryChunk(0x00E000, 57344)
HALL_OF_FAME = BinaryChunk(0x01C000, 8192)
MYSTERY_GIFT = BinaryChunk(0x01E000, 4096)
RECORDED_BATTLE = BinaryChunk(0x01F000, 4096)
