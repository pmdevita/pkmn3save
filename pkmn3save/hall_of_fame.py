from .mapping import HALL_OF_FAME


class HallOfFame:
    def __init__(self, data: bytes):
        self.data = data
        assert len(self.data) == HALL_OF_FAME.size

    @classmethod
    def from_save_file(cls, data: bytes) -> 'HallOfFame':
        return cls(HALL_OF_FAME(data))



